import { redirect } from 'next/navigation';
import { PageShell } from '@/components/page-shell';
import { prisma } from '@/lib/db';
import { getCurrentUser } from '@/lib/session';
import { saveUploadedVideo } from '@/lib/storage';

async function createModuleAction(formData: FormData) {
  'use server';
  const user = await getCurrentUser();
  if (!user || !['admin', 'ceo'].includes(user.role)) redirect('/login');
  const title = String(formData.get('title') || '').trim();
  const description = String(formData.get('description') || '').trim();
  const order = Number(formData.get('order') || 0);
  const required = String(formData.get('required') || 'true') === 'true';
  const file = formData.get('video');
  if (!title || !description || !(file instanceof File) || file.size === 0) redirect('/admin/modules?error=missing');
  const videoUrl = await saveUploadedVideo(file, 'modules');
  const slug = title.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
  await prisma.trainingModule.create({ data: { title, slug, description, videoUrl, order, required } });
  redirect('/admin/modules?created=1');
}

async function updateModuleAction(formData: FormData) {
  'use server';
  const user = await getCurrentUser();
  if (!user || !['admin', 'ceo'].includes(user.role)) redirect('/login');
  const id = String(formData.get('id') || '');
  const title = String(formData.get('title') || '').trim();
  const description = String(formData.get('description') || '').trim();
  const order = Number(formData.get('order') || 0);
  const required = String(formData.get('required') || 'true') === 'true';
  const module = await prisma.trainingModule.findUnique({ where: { id } });
  if (!module || !title || !description) redirect('/admin/modules?error=missing');
  await prisma.trainingModule.update({ where: { id }, data: { title, description, order, required } });
  redirect('/admin/modules?updated=1');
}

async function deleteModuleAction(formData: FormData) {
  'use server';
  const user = await getCurrentUser();
  if (!user || !['admin', 'ceo'].includes(user.role)) redirect('/login');
  const id = String(formData.get('id') || '');
  if (!id) redirect('/admin/modules?error=missing');
  await prisma.trainingModule.delete({ where: { id } });
  redirect('/admin/modules?deleted=1');
}

export default async function AdminModulesPage() {
  const user = await getCurrentUser();
  if (!user) redirect('/login');
  if (!['admin', 'ceo'].includes(user.role)) redirect('/dashboard');
  const modules = await prisma.trainingModule.findMany({ orderBy: { order: 'asc' } });
  return (
    <PageShell title="Manage training modules" description="Upload and organize onboarding content.">
      <div className="grid gap-6 lg:grid-cols-[1fr_1.2fr]">
        <div className="card p-6">
          <h2 className="text-lg font-semibold text-slate-900">Add module</h2>
          <form action={createModuleAction} className="mt-4 space-y-4" encType="multipart/form-data">
            <div><label className="mb-2 block text-sm font-medium text-slate-700">Title</label><input className="input" name="title" required /></div>
            <div><label className="mb-2 block text-sm font-medium text-slate-700">Description</label><textarea className="input min-h-[100px]" name="description" required /></div>
            <div className="grid grid-cols-2 gap-4"><div><label className="mb-2 block text-sm font-medium text-slate-700">Order</label><input className="input" name="order" type="number" defaultValue={5} /></div><div><label className="mb-2 block text-sm font-medium text-slate-700">Required</label><select className="input" name="required" defaultValue="true"><option value="true">Yes</option><option value="false">No</option></select></div></div>
            <div><label className="mb-2 block text-sm font-medium text-slate-700">Video file</label><input className="block w-full text-sm text-slate-600" name="video" type="file" accept="video/*" required /></div>
            <button className="button w-full" type="submit">Upload module</button>
          </form>
        </div>
        <div className="space-y-4">
          {modules.map((module) => (
            <div key={module.id} className="card p-5 space-y-4">
              <div className="flex items-start justify-between gap-4">
                <div>
                  <h3 className="font-semibold text-slate-900">{module.title}</h3>
                  <p className="text-sm text-slate-600">{module.description}</p>
                </div>
                <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-600">{module.slug}</span>
              </div>
              <div className="text-sm text-slate-500">{module.required ? 'Required' : 'Optional'} · {module.videoUrl}</div>
              <form action={updateModuleAction} className="grid gap-3 rounded-xl border border-slate-200 bg-slate-50 p-4" encType="multipart/form-data">
                <input type="hidden" name="id" value={module.id} />
                <div className="grid gap-3 md:grid-cols-2">
                  <input className="input" name="title" defaultValue={module.title} />
                  <input className="input" name="order" type="number" defaultValue={module.order} />
                </div>
                <textarea className="input min-h-[90px]" name="description" defaultValue={module.description} />
                <div className="grid gap-3 md:grid-cols-2">
                  <select className="input" name="required" defaultValue={module.required ? 'true' : 'false'}>
                    <option value="true">Required</option>
                    <option value="false">Optional</option>
                  </select>
                  <button className="button" type="submit">Save changes</button>
                </div>
              </form>
              <form action={deleteModuleAction}>
                <input type="hidden" name="id" value={module.id} />
                <button className="button-secondary" type="submit">Delete module</button>
              </form>
            </div>
          ))}
        </div>
      </div>
    </PageShell>
  );
}
