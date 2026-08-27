"use client";

import { useEffect, useState } from "react";

type Tier="LOW"|"MODERATE"|"HIGH";

type Showcase={
  id: string;
  title: string;
  expected: Tier;
  work_a: string;
  work_b: string;
  analysis: {
    risk: { score: number; tier: Tier; components: Record<string, number> };
    legal: { ordinary_observer_narrative: string; fair_use_consideration: string };
  };
};

const tierChip: Record<Tier, string>={
  LOW: "bg-green-100 text-green-800",
  MODERATE: "bg-amber-100 text-amber-800",
  HIGH: "bg-red-100 text-red-800",
};

const tierBox: Record<Tier, string> = {
  LOW: "bg-green-50 border-green-300 text-green-900",
  MODERATE: "bg-amber-50 border-amber-300 text-amber-900",
  HIGH: "bg-red-50 border-red-300 text-red-900",
};

const FACTOR_LABELS: [string, string][]=[
  ["semantic", "Semantic similarity"],
  ["verbatim", "Verbatim overlap"],
  ["protectability", "Protected-expression ratio"],
  ["literal_pathway", "Literal pathway"],
  ["nonliteral_pathway", "Non-literal pathway"],
];

function Bar({ label, value }: { label: string; value: number }) {
  const pct=Math.round(Math.max(0, Math.min(1, value))*100);
  return (
    <div>
      <div className="flex justify-between text-xs text-gray-600">
        <span>{label}</span>
        <span>{pct}%</span>
      </div>
      <div className="mt-1 h-2 w-full rounded bg-gray-100">
        <div className="h-2 rounded bg-gray-800" style={{ width: `${pct}%` }}/>
      </div>
    </div>
  );
}

function divergenceCaption(semantic: number, tier: Tier): string {
  if (tier=="LOW" && semantic>=0.6)
    return "Highly similar in meaning, yet low in legal risk. The shared material is largely unprotectable (facts, ideas or genre-standard elements). Copyright protects expression, not ideas.";
  if (tier=="HIGH")
    return "Highly similarity that also coppies protectable expression. The overlap isn't just shared facts or ideas.";
  return "Copyright protects expression, not ideas or facts, so semantic similarity and legal risk don't always move together";
}

function Results({ c }: { c: Showcase }) {
  const { risk, legal }=c.analysis;
  const semantic=risk.components.semantic ?? 0;
  const semanticPct=Math.round(semantic*100);

  return (
    <section className="space-y-5">
      {/* verdict */}
      <div className={`rounded-lg border p-5 ${tierBox[risk.tier]}`}>
        <div className="text-sm uppercase tracking-wide opacity-70">
          Copyright-risk verdict
        </div>
        <div className="mt-1 flex items-baseline gap-3">
          <span className="text-3xl font-bold>">{risk.tier}</span>
          <span className="text-lg opacity-70">score {risk.score}</span>
        </div>
      </div>

      {/* divergence callout */}
      <div className="rounded-lg border-2 border-indigo-200 bd-indigo-50 p-5">
        <div className="text-xs font-semibold uppercase tracking-wide text-indigo-700">
          Similarity vs. legal risk
        </div>
        <div className="mt-2 flex items-center gap-5">
          <div>
            <div className="text-2xl font-bold text-indigo-900">
              {semanticPct}%
            </div>
            <div className="text-xs text-indogo-700">semantic similarity</div>
          </div>
          <div className="text-2xl text-indigo-300">→</div>
          <div>
            <div className="text-2xl font-bold text-indigo-900">
              {risk.tier}
            </div>
            <div className="text-xs text-indigo-700">legal risk</div>
          </div>
        </div>
        <p className="mt-3 text-sm text-indigo-900">
          {divergenceCaption(semantic, risk.tier)}
        </p>
      </div>


      {/* works */}
      <div className="mt-5 grdi gap-4 sm:grid-cols-2">
        <div className="rounded border border-gray-200 p-4">
          <div className="mb-2 text-sm font-semibold text-gray-500">
            Work A (suspect)
          </div>
          <p className="text-sm leading-relaxed">{c.work_a}</p>
        </div>
        <div className="rounded border border-gray-200 p-4">
          <div className="mb-2 text-sm font-semibold text-gray-500">
            Work B (original)
          </div>
          <p className="text-sm leading-relaxed">{c.work_b}</p>
        </div>
      </div>

      {/* factor bars */}
      <div className="rounded border border-gray-200 p-4">
        <div className="mb-3 text-sm font-semibold text-gray-500">
          Signal breakdown
        </div>
        <div className="space-y-3">
          {FACTOR_LABELS.filter(([k]) => k in risk.components).map(
            ([key, label]) => (
            <Bar key={key} label={label} value={risk.components[key]} />
          ),
        )}
        </div>
      </div>

      {/* ordinary observer narrative */}
      <div className="rounded border border-gray-200 p-4">
        <div className="mb-2 text-sm font-semibold text-gray-500">
          Ordinary observer
        </div>
        <p className="text-sm leading-relaxed">
          {legal.ordinary_observer_narrative}
        </p>
      </div>

      {/* fair use flag */}
      {legal.fair_use_consideration && (
        <div className="rounded border border-amber-200 bg-amber-50 p-4">
          <div className="mb-1 text-sm font-semibold text-amber-800">
            Fair-use consideration (flagged, not scored)
          </div>
          <p className="text-sm leading-relaxed text-amber-900">
            {legal.fair_use_consideration}
          </p>
        </div>
      )}
    </section>
  );
}

export default function Home() {
  const [cases, setCases]=useState<Showcase[]>([]);
  const [selectedId, setSelectedId]=useState<string | null>(null);
  const [error, setError]=useState<string | null>(null);

  useEffect(() => {
    fetch("/showcases.json")
      .then((r) => r.json())
      .then((data: Showcase[]) => {
        setCases(data);
        setSelectedId(data[0]?.id ?? null);
      })
      .catch((e) => setError(String(e)));
  }, []);

  const selected=cases.find((c) => c.id ===selectedId) ?? null;

  return (
    <main className="mx-auto max-w-3xl p-8">
      <h1 className="text-2xl font-bold">Ordinary Observer</h1>
      <p className="mt-1 text-gray-600">Does one work infringe another? A copyright-risk read on two texts.</p>

      {error && <p className="mt-4 text-red-600">Failed to load: {error}</p>}

      <div className="mt-6 grid gap-6 md:grid-cols-[280px_1fr]">
        <ul className="space-y-2">
          {cases.map((c) => (
            <li key={c.id}>
              <button
                onClick={() => setSelectedId(c.id)}
                className={`flex w-full items-center justify-between rounded border p-3 text-left transition ${
                  c.id===selectedId
                    ? "border-black bg-gray-50"
                    : "border-gray-200 hover:border-gray-400"
                }`}
              >
                <span className="text-sm">{c.title}</span>
                <span className={`rounded px-2 py-0.5 text-xs font-semibold ${tierChip[c.analysis.risk.tier]}`}>
                  {c.analysis.risk.tier}
                </span>
              </button>
            </li>
          ))}
        </ul>
        {selected && <Results c={selected} />}
      </div>

      <footer className="mt-10 border-t pt-4 text-xs text-gray-400">
        Reserach and educational tool. Not legal advice. Analyses are model-generated risk signals, not a determination of infringement.
      </footer>

    </main>
  );
}