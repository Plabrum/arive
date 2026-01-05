/**
 * US State flag/icon component
 * For now, shows a simple map pin icon with state abbreviation
 * Can be enhanced with actual state flags in the future
 */

import { MapPin } from 'lucide-react';

interface StateFlagProps {
  state: string;
  className?: string;
}

export function StateFlag({ state, className = 'h-4 w-4' }: StateFlagProps) {
  return (
    <div className="flex items-center gap-1">
      <MapPin className={className} />
    </div>
  );
}
