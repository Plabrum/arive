import { User, Mail, Phone, MapPin } from 'lucide-react';
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import type { RosterSchema } from '@/openapi/ariveAPI.schemas';

interface CreatorDetailsLayoutProps {
  roster: RosterSchema;
}

export function CreatorDetailsLayout({ roster }: CreatorDetailsLayoutProps) {
  // TODO: Replace with real data from backend once available
  const socialMetrics = {
    totalFollowers: 0,
    platforms: [
      { name: 'Instagram', count: 0, engagementRate: '0%', avgViews: 0 },
      { name: 'TikTok', count: 0, engagementRate: '0%', avgViews: 0 },
      { name: 'YouTube', count: 0, engagementRate: '0%', avgViews: 0 },
    ],
  };

  const revenueStats = {
    total: '$0',
  };

  const campaignsData = {
    waitingForCreator: [],
    allCampaigns: [],
  };

  const accountsReceivable = [
    { amount: '$0', label: 'Pending' },
    { amount: '$0', label: 'Overdue' },
  ];

  return (
    <div className="grid grid-cols-1 gap-6 lg:grid-cols-[2fr_3fr]">
      {/* Left Column */}
      <div className="space-y-6">
        {/* Profile Photo & Contact Info Combined */}
        <Card>
          <CardContent className="p-6">
            <div className="flex gap-4">
              {/* Photo - Small square on left */}
              <div className="flex-shrink-0">
                {roster.profile_photo_id ? (
                  <img
                    src={`/api/media/${roster.profile_photo_id}/view`}
                    alt={roster.name}
                    className="h-20 w-20 rounded-lg object-cover"
                  />
                ) : (
                  <div className="bg-muted flex h-20 w-20 items-center justify-center rounded-lg">
                    <User className="text-muted-foreground h-10 w-10" />
                  </div>
                )}
              </div>

              {/* Right side - Name and contact info with icons */}
              <div className="flex-1 space-y-2">
                <div className="font-semibold text-lg">{roster.name}</div>

                {roster.email && (
                  <div className="flex items-center gap-2 text-muted-foreground text-sm">
                    <Mail className="h-4 w-4" />
                    <span>{roster.email}</span>
                  </div>
                )}

                {roster.phone && (
                  <div className="flex items-center gap-2 text-muted-foreground text-sm">
                    <Phone className="h-4 w-4" />
                    <span>{roster.phone}</span>
                  </div>
                )}

                {roster.address && (
                  <div className="flex items-center gap-2 text-muted-foreground text-sm">
                    <MapPin className="h-4 w-4" />
                    <span>
                      {[
                        roster.address.street_address,
                        roster.address.city,
                        roster.address.state,
                        roster.address.zip_code,
                      ]
                        .filter(Boolean)
                        .join(', ')}
                    </span>
                  </div>
                )}
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Social Follower Overview */}
        <Card>
          <CardHeader>
            <CardTitle className="text-base">
              Social Follower Counts Overview
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-center">
              <div className="text-3xl font-bold">
                {socialMetrics.totalFollowers.toLocaleString()}
              </div>
              <div className="text-muted-foreground text-sm">Total Followers</div>
            </div>
          </CardContent>
        </Card>

        {/* Platform Breakdown */}
        <Card>
          <CardContent className="p-0">
            <div className="divide-y">
              {socialMetrics.platforms.map((platform) => (
                <div
                  key={platform.name}
                  className="grid grid-cols-3 gap-4 px-6 py-4 text-sm"
                >
                  <div className="font-medium">{platform.name}</div>
                  <div className="text-muted-foreground text-center">
                    {platform.count.toLocaleString()} | {platform.engagementRate}
                  </div>
                  <div className="text-muted-foreground text-right">
                    Avg {platform.avgViews.toLocaleString()} views
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Social Cover Photos */}
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Social Cover Photos</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-3 gap-4">
              {[1, 2, 3].map((i) => (
                <div
                  key={i}
                  className="bg-muted flex aspect-square items-center justify-center rounded-lg"
                >
                  <span className="text-muted-foreground text-xs">
                    Cover {i}
                  </span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Right Column */}
      <div className="space-y-6">
        {/* Revenue Stats */}
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Revenue Stats</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-center">
              <div className="text-4xl font-bold">{revenueStats.total}</div>
              <div className="text-muted-foreground text-sm">Total Revenue</div>
            </div>
          </CardContent>
        </Card>

        {/* Campaigns */}
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Campaigns</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {/* Waiting for Creator */}
            <div className="border rounded-lg p-4">
              <div className="text-muted-foreground mb-2 text-sm font-medium">
                Status: Waiting for Creator
              </div>
              {campaignsData.waitingForCreator.length === 0 ? (
                <div className="text-muted-foreground text-center text-sm">
                  No campaigns waiting
                </div>
              ) : (
                <div className="space-y-2">
                  {campaignsData.waitingForCreator.map((campaign: string, i: number) => (
                    <div key={i} className="border rounded p-3 text-sm">
                      {campaign}
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* All Campaigns */}
            <div className="space-y-2">
              <div className="text-sm font-medium">All Campaigns</div>
              {campaignsData.allCampaigns.length === 0 ? (
                <div className="text-muted-foreground text-center text-sm">
                  No active campaigns
                </div>
              ) : (
                <div className="space-y-2">
                  {campaignsData.allCampaigns.map((campaign: string, i: number) => (
                    <div key={i} className="border rounded-lg p-3 text-sm">
                      {campaign}
                    </div>
                  ))}
                </div>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Accounts Receivable */}
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Accounts Receivable</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {accountsReceivable.map((item, i) => (
              <div key={i} className="border rounded-lg p-4 text-center">
                <div className="text-2xl font-bold">{item.amount}</div>
                <div className="text-muted-foreground text-sm">{item.label}</div>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
