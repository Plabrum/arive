import { DollarSign, TrendingUp, Users, Eye, Heart, BarChart3 } from 'lucide-react';
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import type { RosterSchema } from '@/openapi/ariveAPI.schemas';

interface CreatorMetricsProps {
  roster: RosterSchema;
}

interface MetricItemProps {
  icon: React.ReactNode;
  label: string;
  value: string | number;
  subtext?: string;
}

function MetricItem({ icon, label, value, subtext }: MetricItemProps) {
  return (
    <div className="flex items-start gap-3">
      <div className="bg-muted flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-lg">
        {icon}
      </div>
      <div className="flex-1 space-y-1">
        <div className="text-muted-foreground text-sm">{label}</div>
        <div className="text-xl font-semibold">{value}</div>
        {subtext && (
          <div className="text-muted-foreground text-xs">{subtext}</div>
        )}
      </div>
    </div>
  );
}

export function CreatorMetrics({ roster: _roster }: CreatorMetricsProps) {
  // TODO: Replace with real data from backend once available
  // These are placeholder values to demonstrate the UI structure
  // The roster prop will be used once backend metrics are available
  const financialMetrics = {
    totalRevenue: '$0',
    activeCampaigns: 0,
    accountsReceivable: '$0',
    accountsPayable: '$0',
  };

  const socialMetrics = {
    totalFollowers: 0,
    engagementRate: '0%',
    avgViews: 0,
    recentContent: 0,
  };

  return (
    <div className="space-y-6">
      {/* Financial Metrics */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <DollarSign className="h-5 w-5" />
            Financial Performance
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <MetricItem
            icon={<TrendingUp className="text-muted-foreground h-5 w-5" />}
            label="Total Revenue"
            value={financialMetrics.totalRevenue}
            subtext="All-time earnings"
          />
          <MetricItem
            icon={<BarChart3 className="text-muted-foreground h-5 w-5" />}
            label="Active Campaigns"
            value={financialMetrics.activeCampaigns}
            subtext="Currently running"
          />
          <MetricItem
            icon={<DollarSign className="text-muted-foreground h-5 w-5" />}
            label="Accounts Receivable"
            value={financialMetrics.accountsReceivable}
            subtext="Pending payments"
          />
          <MetricItem
            icon={<DollarSign className="text-muted-foreground h-5 w-5" />}
            label="Accounts Payable"
            value={financialMetrics.accountsPayable}
            subtext="Owed to creator"
          />
        </CardContent>
      </Card>

      {/* Social Media Performance */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Users className="h-5 w-5" />
            Social Performance
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <MetricItem
            icon={<Users className="text-muted-foreground h-5 w-5" />}
            label="Total Followers"
            value={socialMetrics.totalFollowers.toLocaleString()}
            subtext="Across all platforms"
          />
          <MetricItem
            icon={<Heart className="text-muted-foreground h-5 w-5" />}
            label="Engagement Rate"
            value={socialMetrics.engagementRate}
            subtext="Avg. across platforms"
          />
          <MetricItem
            icon={<Eye className="text-muted-foreground h-5 w-5" />}
            label="Average Views"
            value={socialMetrics.avgViews.toLocaleString()}
            subtext="Last 10 videos"
          />
          <MetricItem
            icon={<BarChart3 className="text-muted-foreground h-5 w-5" />}
            label="Recent Content"
            value={socialMetrics.recentContent}
            subtext="Last 30 days"
          />
        </CardContent>
      </Card>
    </div>
  );
}
