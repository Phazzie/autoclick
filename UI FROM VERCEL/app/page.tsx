import AutoClickApp from "@/components/auto-click-app"

export default function Home() {
  return (
    <main className="min-h-screen bg-background overflow-hidden">
      <div className="absolute inset-0 -z-10 bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-purple-900 via-slate-900 to-black"></div>
      <div className="absolute inset-0 -z-10 bg-[url('/grid.svg')] bg-center [mask-image:radial-gradient(ellipse_at_center,white,transparent_75%)] opacity-20"></div>
      <AutoClickApp />
    </main>
  )
}

