import { redirect } from 'next/navigation';
import { PageShell } from '@/components/page-shell';
import { ModuleCard } from '@/components/module-card';
import { prisma } from '@/lib/db';
import { getCurrentUser } from '@/lib/session';

export default async function DashboardPage() {
  const user = await getCurrentUser();
  if (!user) redirect('/login');
  const modules = await prisma.trainingModule.findMany({ orderBy: { order: 'asc' } });
  const completions = await prisma.completion.findMany({ where: { userId: user.id } });
  const completionSet = new Set(completions.filter((c) => c.completedAt).map((c) => c.moduleId));
  const decorated = modules.map((module) => ({ ...module, completed: completionSet.has(module.id) }));
  return (
    <PageShell title="Training dashboard" description="Required onboarding modules for new hires.">
      <div className="mb-6 grid gap-4 md:grid-cols-3">
        <div className="card p-5"><div className="text-sm text-slate-500">Logged in as</div><div className="mt-1 text-xl font-semibold text-slate-900">{user.name}</div><div className="text-sm text-slate-500">{user.email}</div></div>
        <div className="card p-5"><div className="text-sm text-slate-500">Required modules</div><div className="mt-1 text-3xl font-bold text-slate-900">{decorated.filter((m) => m.required).length}</div></div>
        <div className="card p-5"><div className="text-sm text-slate-500">Completed</div><div className="mt-1 text-3xl font-bold text-slate-900">{decorated.filter((m) => m.completed).length}</div></div>
      </div>
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">{decorated.map((module) => <ModuleCard key={module.id} module={module} />)}</div>
    </PageShell>
  );
}
