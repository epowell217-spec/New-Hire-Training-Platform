import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Center of Family Love Training',
  description: 'Employee training portal for onboarding, compliance, and leadership updates.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
