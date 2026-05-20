import { Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Activity, GitMerge, Box, Cpu } from "lucide-react";
import { fetchHealth } from "@/lib/api";
import { Badge } from "@/components/ui/badge";

export function Dashboard() {
  const health = useQuery({ queryKey: ["health"], queryFn: fetchHealth, refetchInterval: 10000 });

  const bcOk = health.data?.beyond_compare.detected ?? false;
  const version = health.data?.server.version ?? "…";

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight text-white">Compare Dashboard</h2>
          <p className="text-slate-400">Unified gateway · v{version}</p>
        </div>
        <Badge variant="outline" className="border-slate-600 text-slate-200">
          {health.isFetching ? "refreshing" : "live"}
        </Badge>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card className="border-slate-800 bg-slate-950/50">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-slate-200">Gateway</CardTitle>
            <Cpu className="h-4 w-4 text-emerald-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-white">{health.isError ? "offline" : "online"}</div>
            <p className="text-xs text-slate-400">{health.isError ? (health.error as Error).message : "REST + MCP on 10841"}</p>
          </CardContent>
        </Card>

        <Card className="border-slate-800 bg-slate-950/50">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-slate-200">Compare engine</CardTitle>
            <Activity className="h-4 w-4 text-blue-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-white">{bcOk ? "Ready" : "Not found"}</div>
            <p className="text-xs text-slate-400 truncate">{health.data?.beyond_compare.executable ?? "—"}</p>
          </CardContent>
        </Card>

        <Card className="border-slate-800 bg-slate-950/50">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-slate-200">Scripts dir</CardTitle>
            <Box className="h-4 w-4 text-purple-500" />
          </CardHeader>
          <CardContent>
            <div className="text-sm font-mono text-slate-200 truncate">{health.data?.beyond_compare.scripts_dir ?? "—"}</div>
            <p className="text-xs text-slate-400">BC temp scripts</p>
          </CardContent>
        </Card>

        <Card className="border-slate-800 bg-slate-950/50">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-slate-200">Fleet</CardTitle>
            <GitMerge className="h-4 w-4 text-orange-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-white">10840 / 10841</div>
            <p className="text-xs text-slate-400">UI / gateway</p>
          </CardContent>
        </Card>
      </div>

      <Card className="border-slate-800 bg-slate-950/50">
        <CardHeader>
          <CardTitle className="text-white">Quick links</CardTitle>
        </CardHeader>
        <CardContent className="text-sm text-slate-400 space-y-2">
          <p>
            <Link className="text-blue-400 hover:underline" to="/actions">
              Actions
            </Link>{" "}
            — tool surface and health detail
          </p>
          <p>
            <Link className="text-blue-400 hover:underline" to="/logs">
              Logs
            </Link>{" "}
            — gateway request ring buffer
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
