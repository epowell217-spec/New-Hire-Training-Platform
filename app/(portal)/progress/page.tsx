import { redirect } from 'next/navigation';
import { PageShell } from '@/components/page-shell';
import { prisma } from '@/lib/db';
import { getCurrentUser } from '@/lib/session';

export default async function ProgressPage() {
  const user = await getCurrentUser();
  if (!user) redirect('/login');
  const modules = await prisma.trainingModule.findMany({ orderBy: { order: 'asc' } });
  const completions = await prisma.completion.findMany({ where: { userId: user.id } });
  const completionSet = new Set(completions.filter((c) => c.completedAt).map((c) => c.moduleId));
  const required = modules.filter((module) => module.required);
  const completed = required.filter((module) => completionSet.has(module.id)).length;
  const pct = required.length === 0 ? 0 : Math.round((completed / required.length) * 100);
  return (
    <PageShell title="My progress" description="Completion status for required training modules.">
      <div className="card p-6">
        <div className="flex items-center justify-between">
          <div><div className="text-sm text-slate-500">Progress</div><div className="mt-1 text-3xl font-bold text-slate-900">{pct}%</div></div>
          <div className="text-right text-sm text-slate-500"><div>{completed} of {required.length} required modules complete</div></div>
        </div>
        <div className="mt-4 h-3 rounded-full bg-slate-100"><div className="h-3 rounded-full bg-brand-600" style={{ width: `${pct}%` }} /></div>
      </div>
    </PageShell>
  );
}
