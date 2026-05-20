import { useQuery } from "@tanstack/react-query";
import { fetchCapabilities, fetchHealth } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export function Actions() {
  const health = useQuery({ queryKey: ["health"], queryFn: fetchHealth, refetchInterval: 8000 });
  const cap = useQuery({ queryKey: ["capabilities"], queryFn: fetchCapabilities, refetchInterval: 60000 });

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold tracking-tight text-white">Fleet actions</h2>
        <p className="text-slate-400">Live gateway status and MCP tool surface</p>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <Card className="border-slate-800 bg-slate-950/50">
          <CardHeader>
            <CardTitle className="text-white">Gateway health</CardTitle>
            <CardDescription className="text-slate-400">GET /api/v1/health</CardDescription>
          </CardHeader>
          <CardContent className="space-y-2 text-sm text-slate-300">
            {health.isLoading && <p>Loading…</p>}
            {health.isError && <p className="text-rose-400">{(health.error as Error).message}</p>}
            {health.data && (
              <>
                <p>
                  Beyond Compare:{" "}
                  <Badge variant="outline" className="border-slate-600 text-slate-200">
                    {health.data.beyond_compare.detected ? "detected" : "missing"}
                  </Badge>
                </p>
                <p className="font-mono text-xs break-all">{health.data.beyond_compare.executable}</p>
                <p className="text-slate-500">Uptime {Math.round(health.data.system.uptime_s)}s</p>
              </>
            )}
          </CardContent>
        </Card>

        <Card className="border-slate-800 bg-slate-950/50">
          <CardHeader>
            <CardTitle className="text-white">MCP tools</CardTitle>
            <CardDescription className="text-slate-400">GET /api/capabilities</CardDescription>
          </CardHeader>
          <CardContent>
            {cap.isLoading && <p className="text-slate-400">Loading…</p>}
            {cap.isError && <p className="text-rose-400">{(cap.error as Error).message}</p>}
            {cap.data && (
              <div className="space-y-2 text-xs text-slate-400">
                <p className="text-slate-300">Atomic ({cap.data.tool_surface.atomic.length})</p>
                <p className="font-mono break-all">{cap.data.tool_surface.atomic.join(", ")}</p>
                <p className="text-slate-300 pt-2">Agentic</p>
                <p className="font-mono break-all">{cap.data.tool_surface.agentic.join(", ")}</p>
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      <Card className="border-slate-800 bg-slate-950/50">
        <CardHeader>
          <CardTitle className="text-white">Using from Cursor / Claude</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2 text-sm text-slate-400">
          <p>
            MCP endpoint (HTTP): <code className="text-slate-200">http://127.0.0.1:10841/mcp</code> (default path; set{" "}
            <code className="text-slate-200">MCP_PATH</code> if overridden).
          </p>
          <p>
            For multi-step natural language goals, call <code className="text-slate-200">beyondcompare_agentic_workflow</code>{" "}
            when your client supports sampling.
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
