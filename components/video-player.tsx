export function VideoPlayer({ src, title }: { src: string; title: string }) {
  return (
    <div className="overflow-hidden rounded-2xl border border-slate-200 bg-black shadow-sm">
      <video className="h-auto w-full" controls preload="metadata" src={src} aria-label={title} />
    </div>
  );
}
