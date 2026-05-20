import { useEffect, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { fetchHealth, fetchLlmSettings, fetchOllamaModels, saveLlmSettings } from "@/lib/api";

export function Settings() {
  const qc = useQueryClient();
  const health = useQuery({ queryKey: ["health"], queryFn: fetchHealth, refetchInterval: 15000 });
  const models = useQuery({ queryKey: ["ollama-models"], queryFn: fetchOllamaModels, refetchInterval: 30000 });
  const llm = useQuery({ queryKey: ["llm-settings"], queryFn: fetchLlmSettings });
  const [model, setModel] = useState("");
  const [provider, setProvider] = useState("ollama");

  useEffect(() => {
    if (llm.data) {
      setModel(llm.data.model ?? "");
      setProvider(llm.data.provider ?? "ollama");
    }
  }, [llm.data]);

  const save = useMutation({
    mutationFn: () => saveLlmSettings({ model, provider }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["llm-settings"] }),
  });

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold tracking-tight text-white">Settings</h2>
        <p className="text-slate-400">Gateway-detected Beyond Compare and local LLM preferences (Ollama)</p>
      </div>

      <div className="grid gap-6">
        <Card className="border-slate-800 bg-slate-950/50">
          <CardHeader>
            <CardTitle className="text-white">Beyond Compare</CardTitle>
            <CardDescription className="text-slate-400">From GET /api/v1/health (server process)</CardDescription>
          </CardHeader>
          <CardContent className="space-y-2 text-sm text-slate-300">
            {health.isLoading && <p>Loading…</p>}
            {health.isError && <p className="text-rose-400">{(health.error as Error).message}</p>}
            {health.data && (
              <>
                <p>Detected: {health.data.beyond_compare.detected ? "yes" : "no"}</p>
                <p className="font-mono text-xs break-all text-slate-400">{health.data.beyond_compare.executable}</p>
                <p className="text-xs text-slate-500">
                  Override with env <code className="text-slate-300">BEYOND_COMPARE_PATH</code> and restart the gateway.
                </p>
              </>
            )}
          </CardContent>
        </Card>

        <Card className="border-slate-800 bg-slate-950/50">
          <CardHeader>
            <CardTitle className="text-white">Local LLM (Ollama)</CardTitle>
            <CardDescription className="text-slate-400">
              Model list is probed at <code className="text-slate-300">OLLAMA_BASE_URL</code> (default 127.0.0.1:11434)
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid gap-2">
              <Label className="text-slate-300">Provider</Label>
              <Input
                value={provider}
                onChange={(e) => setProvider(e.target.value)}
                className="bg-slate-900 border-slate-800 text-slate-100"
              />
            </div>
            <div className="grid gap-2">
              <Label className="text-slate-300">Model name</Label>
              <Input
                value={model}
                onChange={(e) => setModel(e.target.value)}
                placeholder="llama3.2"
                className="bg-slate-900 border-slate-800 text-slate-100"
              />
            </div>
            {models.data && (
              <p className="text-xs text-slate-500">
                Ollama tags: {models.data.ok ? models.data.models.slice(0, 8).join(", ") : models.data.error || "unavailable"}
              </p>
            )}
            <Button
              type="button"
              variant="outline"
              className="border-slate-800 text-slate-300 hover:bg-slate-800"
              disabled={save.isPending}
              onClick={() => save.mutate()}
            >
              {save.isPending ? "Saving…" : "Save LLM preferences"}
            </Button>
            {save.isSuccess && <p className="text-xs text-emerald-400">Saved to in-memory gateway store.</p>}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
