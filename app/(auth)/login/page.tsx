import Link from 'next/link';
import { redirect } from 'next/navigation';
import bcrypt from 'bcryptjs';
import { PageShell } from '@/components/page-shell';
import { prisma } from '@/lib/db';
import { getCurrentUser, createSessionToken, setSessionCookie } from '@/lib/session';

async function loginAction(formData: FormData) {
  'use server';
  const email = String(formData.get('email') || '').trim().toLowerCase();
  const password = String(formData.get('password') || '');
  const user = await prisma.user.findUnique({ where: { email } });
  if (!user || !user.passwordHash || !user.active) redirect('/login?error=invalid');
  const ok = await bcrypt.compare(password, user.passwordHash);
  if (!ok) redirect('/login?error=invalid');
  setSessionCookie(createSessionToken(user.id));
  redirect('/dashboard');
}

export default async function LoginPage({ searchParams }: { searchParams: Promise<{ error?: string }> }) {
  const user = await getCurrentUser();
  if (user) redirect('/dashboard');
  const params = await searchParams;
  return (
    <PageShell title="Login" description="Employees sign in with their email and password.">
      <div className="card mx-auto max-w-md p-6">
        <form action={loginAction} className="space-y-4">
          <div>
            <label className="mb-2 block text-sm font-medium text-slate-700">Email</label>
            <input className="input" name="email" type="email" placeholder="name@company.org" required />
          </div>
          <div>
            <label className="mb-2 block text-sm font-medium text-slate-700">Password</label>
            <input className="input" name="password" type="password" placeholder="••••••••" required />
          </div>
          {params.error ? <p className="text-sm text-red-600">Invalid email or password.</p> : null}
          <button className="button w-full" type="submit">Sign in</button>
        </form>
        <p className="mt-4 text-sm text-slate-500">New hires sign in using the email invite sent to their personal email.</p>
        <p className="mt-2 text-xs text-slate-400">Admin demo users: ceo@example.org / admin@example.org / newhire@example.org</p>
        <Link className="mt-2 inline-block text-sm font-medium" href="/admin/users">Admin user management</Link>
      </div>
    </PageShell>
  );
}
