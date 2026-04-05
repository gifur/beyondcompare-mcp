import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Activity, GitMerge, Box, Cpu } from "lucide-react";

export function Dashboard() {
    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-2xl font-bold tracking-tight text-white">Compare Dashboard</h2>
                    <p className="text-slate-400">File comparison and session status</p>
                </div>
            </div>

            {/* KPI Cards */}
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                <Card className="border-slate-800 bg-slate-950/50">
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium text-slate-200">
                            Active Syncs
                        </CardTitle>
                        <Cpu className="h-4 w-4 text-emerald-500" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold text-white">2</div>
                        <p className="text-xs text-slate-400">
                            Sessions running
                        </p>
                    </CardContent>
                </Card>

                <Card className="border-slate-800 bg-slate-950/50">
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium text-slate-200">
                            Compare Engine
                        </CardTitle>
                        <Activity className="h-4 w-4 text-blue-500" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold text-white">Ready</div>
                        <p className="text-xs text-slate-400">
                            SOTA Performance
                        </p>
                    </CardContent>
                </Card>

                <Card className="border-slate-800 bg-slate-950/50">
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium text-slate-200">
                            Total Diff Count
                        </CardTitle>
                        <Box className="h-4 w-4 text-purple-500" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold text-white">1,204</div>
                        <p className="text-xs text-slate-400">
                            Across all folders
                        </p>
                    </CardContent>
                </Card>

                <Card className="border-slate-800 bg-slate-950/50">
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium text-slate-200">
                            Session Health
                        </CardTitle>
                        <GitMerge className="h-4 w-4 text-orange-500" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold text-white">Optimal</div>
                        <p className="text-xs text-slate-400">
                            Zero collisions detected
                        </p>
                    </CardContent>
                </Card>
            </div>

            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
                <Card className="col-span-4 border-slate-800 bg-slate-950/50">
                    <CardHeader>
                        <CardTitle className="text-white">Active Sessions</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-4">
                            {[1, 2].map((i) => (
                                <div key={i} className="flex items-center gap-4 p-3 rounded-lg bg-slate-900/40 border border-slate-800">
                                    <div className="p-2 rounded bg-blue-500/10">
                                        <Activity className="h-4 w-4 text-blue-500" />
                                    </div>
                                    <div className="flex-1 min-w-0">
                                        <p className="text-sm font-medium text-slate-200 truncate">Session-{i}: Core Refactor</p>
                                        <p className="text-xs text-slate-500 truncate">D:/Dev/repos/project-a vs D:/Dev/repos/project-b</p>
                                    </div>
                                    <div className="text-xs text-emerald-400 font-mono">Comparing...</div>
                                </div>
                            ))}
                        </div>
                    </CardContent>
                </Card>
                <Card className="col-span-3 border-slate-800 bg-slate-950/50">
                    <CardHeader>
                        <CardTitle className="text-white">Recent Sync Operations</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-4">
                            <div className="flex items-center">
                                <span className="relative flex h-2 w-2 mr-2">
                                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                                    <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                                </span>
                                <div className="ml-2 space-y-1">
                                    <p className="text-sm font-medium leading-none text-white">Production Sync</p>
                                    <p className="text-xs text-slate-400">42 files updated • Success</p>
                                </div>
                                <div className="ml-auto font-mono text-xs text-slate-400">04:21</div>
                            </div>
                            <div className="flex items-center">
                                <span className="relative flex h-2 w-2 mr-2 bg-slate-700 rounded-full"></span>
                                <div className="ml-2 space-y-1">
                                    <p className="text-sm font-medium leading-none text-white text-opacity-50">Staging Backup</p>
                                    <p className="text-xs text-slate-500">Idle</p>
                                </div>
                            </div>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
