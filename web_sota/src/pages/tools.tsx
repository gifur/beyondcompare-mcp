import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Wrench, Terminal, Shield, Cpu } from "lucide-react";

export function Tools() {
    const tools = [
        { name: 'Hex Compare', desc: 'Binary byte-by-byte comparison', icon: Terminal },
        { name: 'MP3 Compare', desc: 'Tag and audio data alignment', icon: Cpu },
        { name: 'Text Merge', desc: 'Three-way text reconciliation', icon: Wrench },
        { name: 'Registry Compare', desc: 'Windows registry hive diffing', icon: Shield },
    ];

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-2xl font-bold tracking-tight text-white">Utility Tools</h2>
                    <p className="text-slate-400">Specialized comparison and merging plugins</p>
                </div>
            </div>

            <div className="grid gap-4 md:grid-cols-2">
                {tools.map((tool) => (
                    <Card key={tool.name} className="border-slate-800 bg-slate-950/50 hover:bg-slate-900/50 transition-colors cursor-pointer group">
                        <CardHeader className="flex flex-row items-center gap-4">
                            <div className="p-2 rounded bg-blue-500/10 group-hover:bg-blue-500/20 transition-colors">
                                <tool.icon className="h-6 w-6 text-blue-500" />
                            </div>
                            <div>
                                <CardTitle className="text-white text-lg">{tool.name}</CardTitle>
                                <CardDescription className="text-slate-400">{tool.desc}</CardDescription>
                            </div>
                        </CardHeader>
                    </Card>
                ))}
            </div>
        </div>
    );
}
