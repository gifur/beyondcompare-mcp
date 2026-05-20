import { useQuery } from "@tanstack/react-query";
import { fetchLogs } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";

export function Logs() {
  const q = useQuery({ queryKey: ["logs"], queryFn: () => fetchLogs(300), refetchInterval: 4000 });

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold tracking-tight text-white">Gateway log ring</h2>
        <p className="text-slate-400">Recent HTTP requests and lifecycle events from the unified API (port 10841)</p>
      </div>

      <Card className="border-slate-800 bg-slate-950/50">
        <CardHeader>
          <CardTitle className="text-white">Tail</CardTitle>
        </CardHeader>
        <CardContent>
          {q.isLoading && <p className="text-slate-400">Loading…</p>}
          {q.isError && (
            <p className="text-rose-400">
              {(q.error as Error).message}. Start the gateway:{" "}
              <code className="text-slate-300">uv run python -m beyondcompare_mcp.server --http --port 10841</code>
            </p>
          )}
          {q.data && (
            <ScrollArea className="h-[480px] rounded-md border border-slate-800 bg-slate-900/40 p-3">
              <pre className="text-xs text-slate-300 whitespace-pre-wrap font-mono">
                {JSON.stringify(q.data.entries, null, 2)}
              </pre>
            </ScrollArea>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
