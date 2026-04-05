import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { RefreshCw, Play, RotateCcw } from "lucide-react";

export function Sync() {
    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-2xl font-bold tracking-tight text-white">Folder Synchronization</h2>
                    <p className="text-slate-400">Automated mirror and update tasks</p>
                </div>
                <div className="flex gap-2">
                    <Button variant="outline" className="border-slate-800 text-slate-300 hover:bg-slate-800">
                        <RotateCcw className="mr-2 h-4 w-4" /> Reset All
                    </Button>
                    <Button className="bg-emerald-600 hover:bg-emerald-700">
                        <Play className="mr-2 h-4 w-4" /> Run All Syncs
                    </Button>
                </div>
            </div>

            <div className="grid gap-6">
                <Card className="border-slate-800 bg-slate-950/50">
                    <CardHeader>
                        <CardTitle className="text-white">Sync Tasks</CardTitle>
                        <CardDescription className="text-slate-400">Configured synchronization profiles</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="flex items-center justify-between p-4 rounded-lg bg-slate-900/40 border border-slate-800">
                            <div className="flex items-center gap-4">
                                <div className="p-2 rounded bg-emerald-500/10">
                                    <RefreshCw className="h-5 w-5 text-emerald-500" />
                                </div>
                                <div>
                                    <div className="ml-auto font-mono text-xs text-slate-400">04:21</div>
                                    <p className="text-sm font-medium text-slate-200">{"Mirror: Local -> NAS"}</p>
                                    <p className="text-xs text-slate-500">Status: Idle • Last run: 2h ago</p>
                                </div>
                            </div>
                            <Button size="sm" className="bg-emerald-600/20 text-emerald-400 hover:bg-emerald-600/30">Sync Now</Button>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
