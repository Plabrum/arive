/**
 * US State flag/icon component
 * For now, shows a simple map pin icon
 * Can be enhanced with actual state flags in the future
 */

import { MapPin } from 'lucide-react';

interface StateFlagProps {
  state?: string; // Reserved for future use (state-specific flags)
  className?: string;
}

export function StateFlag({ className = 'h-4 w-4' }: StateFlagProps) {
  return (
    <div className="flex items-center gap-1">
      <MapPin className={className} />
    </div>
  );
}
