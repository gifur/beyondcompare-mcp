import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input"; // We'll need to create this or use standard input
import { Label } from "@/components/ui/label"; // We'll need to create this or use standard label

export function Settings() {
    return (
        <div className="space-y-6">
            <div>
                <h2 className="text-2xl font-bold tracking-tight text-white">Settings</h2>
                <p className="text-slate-400">Manage connections and preferences</p>
            </div>

            <div className="grid gap-6">
                <Card className="border-slate-800 bg-slate-950/50">
                    <CardHeader>
                        <CardTitle className="text-white">Beyond Compare Path</CardTitle>
                        <CardDescription className="text-slate-400">Location of the BComp.exe executable</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="grid gap-2">
                            <Label className="text-slate-300">Executable Path</Label>
                            <Input
                                id="exec-path"
                                title="Beyond Compare Executable Path"
                                placeholder="C:\Program Files\..."
                                className="bg-slate-900 border-slate-800 text-slate-100 placeholder:text-slate-400"
                                defaultValue="C:\Program Files\Beyond Compare 4\BComp.exe"
                            />
                        </div>
                        <Button variant="outline" className="border-slate-800 text-slate-300 hover:bg-slate-800">
                            Auto-Detect
                        </Button>
                    </CardContent>
                </Card>

                <Card className="border-slate-800 bg-slate-950/50">
                    <CardHeader>
                        <CardTitle className="text-white">Comparison Rules</CardTitle>
                        <CardDescription className="text-slate-400">Default behavior for new sessions</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="flex items-center space-x-2">
                            <input type="checkbox" id="binary" title="Binary Comparison" className="rounded border-slate-800 bg-slate-900" defaultChecked />
                            <Label htmlFor="binary" className="text-slate-300">Use binary comparison by default</Label>
                        </div>
                        <div className="flex items-center space-x-2">
                            <input type="checkbox" id="timestamps" title="Ignore Timestamps" className="rounded border-slate-800 bg-slate-900" defaultChecked />
                            <Label htmlFor="timestamps" className="text-slate-300">Ignore timestamp differences</Label>
                        </div>
                        <Button variant="outline" className="border-slate-800 text-slate-300 hover:bg-slate-800">
                            Save Preferences
                        </Button>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
