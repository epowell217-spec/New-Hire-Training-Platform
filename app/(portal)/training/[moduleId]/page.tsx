import { notFound, redirect } from 'next/navigation';
import { PageShell } from '@/components/page-shell';
import { VideoPlayer } from '@/components/video-player';
import { prisma } from '@/lib/db';
import { getCurrentUser } from '@/lib/session';

async function markCompleteAction(moduleId: string) {
  'use server';
  const user = await getCurrentUser();
  if (!user) redirect('/login');
  await prisma.completion.upsert({
    where: { userId_moduleId: { userId: user.id, moduleId } },
    update: { completedAt: new Date(), watchedAt: new Date() },
    create: { userId: user.id, moduleId, watchedAt: new Date(), completedAt: new Date() },
  });
  redirect(`/training/${moduleId}`);
}

export default async function ModulePage({ params }: { params: Promise<{ moduleId: string }> }) {
  const user = await getCurrentUser();
  if (!user) redirect('/login');
  const { moduleId } = await params;
  const module = await prisma.trainingModule.findUnique({ where: { id: moduleId } });
  if (!module) return notFound();
  const completion = await prisma.completion.findUnique({ where: { userId_moduleId: { userId: user.id, moduleId } } });
  const completed = Boolean(completion?.completedAt);
  return (
    <PageShell title={module.title} description={module.description}>
      <div className="grid gap-6 lg:grid-cols-[2fr_1fr]">
        <div className="space-y-4">
          <VideoPlayer src={module.videoUrl} title={module.title} />
          <div className="card p-5">
            <h2 className="text-lg font-semibold text-slate-900">Completion</h2>
            <p className="mt-1 text-sm text-slate-600">Watch the video, then mark the module complete.</p>
            <form action={markCompleteAction.bind(null, module.id)}>
              <button className="button mt-4" type="submit">{completed ? 'Completed' : 'Mark complete'}</button>
            </form>
          </div>
        </div>
        <aside className="card p-5"><h3 className="font-semibold text-slate-900">Module info</h3><dl className="mt-4 space-y-3 text-sm"><div><dt className="text-slate-500">Status</dt><dd className="font-medium text-slate-900">{completed ? 'Completed' : 'Not completed'}</dd></div><div><dt className="text-slate-500">Required</dt><dd className="font-medium text-slate-900">{module.required ? 'Yes' : 'No'}</dd></div></dl></aside>
      </div>
    </PageShell>
  );
}
