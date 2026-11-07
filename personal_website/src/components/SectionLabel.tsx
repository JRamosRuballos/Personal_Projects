/** Shared section heading: section number, rule, display title. */
export function SectionLabel({
  n,
  children,
  id,
}: {
  n: string;
  children: string;
  id?: string;
}) {
  return (
    <div className="mb-10 flex items-baseline gap-4 border-b border-border pb-3">
      <span className="font-mono text-xs text-primary">{n}</span>
      <h2 id={id} className="font-display text-4xl md:text-5xl">
        {children}
      </h2>
    </div>
  );
}
