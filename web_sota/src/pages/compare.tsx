import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Activity, GitCompare, ArrowRight } from "lucide-react";

export function Compare() {
    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-2xl font-bold tracking-tight text-white">Compare Sessions</h2>
                    <p className="text-slate-400">Manage and launch file/folder comparisons</p>
                </div>
                <Button className="bg-blue-600 hover:bg-blue-700">
                    <Activity className="mr-2 h-4 w-4" /> New Session
                </Button>
            </div>

            <div className="grid gap-6">
                <Card className="border-slate-800 bg-slate-950/50">
                    <CardHeader>
                        <CardTitle className="text-white">Active Comparison</CardTitle>
                        <CardDescription className="text-slate-400">Currently open sessions in Beyond Compare</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        {[1, 2].map((i) => (
                            <div key={i} className="flex items-center justify-between p-4 rounded-lg bg-slate-900/40 border border-slate-800">
                                <div className="flex items-center gap-4">
                                    <div className="p-2 rounded bg-blue-500/10">
                                        <GitCompare className="h-5 w-5 text-blue-500" />
                                    </div>
                                    <div>
                                        <p className="text-sm font-medium text-slate-200">Refactor Audit {i}</p>
                                        <div className="flex items-center gap-2 text-xs text-slate-500">
                                            <span>src/core</span>
                                            <ArrowRight className="h-3 w-3" />
                                            <span>backup/src/core</span>
                                        </div>
                                    </div>
                                </div>
                                <Button size="sm" variant="ghost" className="text-blue-400 hover:text-blue-300">View Diffs</Button>
                            </div>
                        ))}
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
