import { Nav } from './nav';

export function PageShell({ children, title, description }: { children: React.ReactNode; title: string; description?: string }) {
  return (
    <div className="min-h-screen">
      <Nav />
      <main className="mx-auto max-w-6xl px-6 py-10">
        <header className="mb-8 space-y-2">
          <h1 className="text-3xl font-bold tracking-tight text-slate-900">{title}</h1>
          {description ? <p className="max-w-3xl text-slate-600">{description}</p> : null}
        </header>
        {children}
      </main>
    </div>
  );
}
