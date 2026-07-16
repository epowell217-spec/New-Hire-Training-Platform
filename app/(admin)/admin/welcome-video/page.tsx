import { redirect } from 'next/navigation';
import { PageShell } from '@/components/page-shell';
import { prisma } from '@/lib/db';
import { getCurrentUser } from '@/lib/session';
import { saveUploadedVideo } from '@/lib/storage';

async function uploadWelcomeVideoAction(formData: FormData) {
  'use server';
  const user = await getCurrentUser();
  if (!user || !['admin', 'ceo'].includes(user.role)) redirect('/login');
  const title = String(formData.get('title') || '').trim() || 'Welcome from our CEO';
  const file = formData.get('video');
  if (!(file instanceof File) || file.size === 0) redirect('/admin/welcome-video?error=file');
  const videoUrl = await saveUploadedVideo(file, 'welcome');
  await prisma.welcomeVideo.create({ data: { title, videoUrl, uploadedById: user.id } });
  redirect('/admin/welcome-video?uploaded=1');
}

export default async function WelcomeVideoPage() {
  const user = await getCurrentUser();
  if (!user) redirect('/login');
  if (!['admin', 'ceo'].includes(user.role)) redirect('/dashboard');
  const latest = await prisma.welcomeVideo.findFirst({ orderBy: { createdAt: 'desc' } });
  return (
    <PageShell title="CEO welcome video" description="Upload a leadership welcome video without touching code.">
      <div className="grid gap-6 lg:grid-cols-[1fr_1fr]">
        <div className="card p-6">
          <h2 className="text-lg font-semibold text-slate-900">Upload new video</h2>
          <form action={uploadWelcomeVideoAction} className="mt-4 space-y-4" encType="multipart/form-data">
            <div><label className="mb-2 block text-sm font-medium text-slate-700">Title</label><input className="input" name="title" defaultValue="Welcome from our CEO" /></div>
            <div><label className="mb-2 block text-sm font-medium text-slate-700">Video file</label><input className="block w-full text-sm text-slate-600" name="video" type="file" accept="video/*" required /></div>
            <button className="button" type="submit">Upload welcome video</button>
          </form>
        </div>
        <div className="card p-6">
          <h2 className="text-lg font-semibold text-slate-900">Latest upload</h2>
          {latest ? <div className="mt-4 space-y-2 text-sm text-slate-600"><div><span className="font-medium text-slate-900">Title:</span> {latest.title}</div><div><span className="font-medium text-slate-900">URL:</span> <a href={latest.videoUrl}>{latest.videoUrl}</a></div></div> : <p className="mt-4 text-sm text-slate-500">No welcome video uploaded yet.</p>}
        </div>
      </div>
    </PageShell>
  );
}
