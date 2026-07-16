import Link from 'next/link';

const links = [
  { href: '/dashboard', label: 'Dashboard' },
  { href: '/progress', label: 'My Progress' },
  { href: '/admin', label: 'Admin' },
  { href: '/login', label: 'Login' },
];

export function Nav() {
  return (
    <nav className="flex flex-wrap items-center gap-3 border-b border-slate-200 bg-white px-6 py-4">
      <div className="mr-auto font-semibold text-slate-900">Center of Family Love</div>
      {links.map((link) => (
        <Link key={link.href} href={link.href} className="rounded-lg px-3 py-2 text-sm font-medium text-slate-600 hover:bg-slate-100 hover:text-slate-900">
          {link.label}
        </Link>
      ))}
      <Link href="/logout" className="rounded-lg px-3 py-2 text-sm font-medium text-slate-600 hover:bg-slate-100 hover:text-slate-900">
        Logout
      </Link>
    </nav>
  );
}
