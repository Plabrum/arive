import { Instagram, Facebook, Youtube, Users } from 'lucide-react';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import type { RosterSchema } from '@/openapi/ariveAPI.schemas';

interface RosterMediaKitProps {
  roster: RosterSchema;
}

interface SocialPlatform {
  name: string;
  handle: string | null | undefined;
  url: string;
  icon: React.ReactNode;
  color: string;
  followers?: number; // Placeholder for future data
}

export function RosterMediaKit({ roster }: RosterMediaKitProps) {
  // Build array of social platforms with URLs
  const platforms: SocialPlatform[] = [
    {
      name: 'Instagram',
      handle: roster.instagram_handle,
      url: roster.instagram_handle
        ? `https://instagram.com/${roster.instagram_handle.replace('@', '')}`
        : '',
      icon: <Instagram className="h-5 w-5" />,
      color: 'text-pink-500',
      followers: 0, // Placeholder
    },
    {
      name: 'TikTok',
      handle: roster.tiktok_handle,
      url: roster.tiktok_handle
        ? `https://tiktok.com/@${roster.tiktok_handle.replace('@', '')}`
        : '',
      icon: (
        <svg className="h-5 w-5" viewBox="0 0 24 24" fill="currentColor">
          <path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-5.2 1.74 2.89 2.89 0 0 1 2.31-4.64 2.93 2.93 0 0 1 .88.13V9.4a6.84 6.84 0 0 0-1-.05A6.33 6.33 0 0 0 5 20.1a6.34 6.34 0 0 0 10.86-4.43v-7a8.16 8.16 0 0 0 4.77 1.52v-3.4a4.85 4.85 0 0 1-1-.1z" />
        </svg>
      ),
      color: 'text-foreground',
      followers: 0, // Placeholder
    },
    {
      name: 'YouTube',
      handle: roster.youtube_channel,
      url: roster.youtube_channel || '',
      icon: <Youtube className="h-5 w-5" />,
      color: 'text-red-500',
      followers: 0, // Placeholder
    },
    {
      name: 'Facebook',
      handle: roster.facebook_handle,
      url: roster.facebook_handle
        ? `https://facebook.com/${roster.facebook_handle}`
        : '',
      icon: <Facebook className="h-5 w-5" />,
      color: 'text-blue-500',
      followers: 0, // Placeholder
    },
  ];

  // Filter to active platforms
  const activePlatforms = platforms.filter((p) => p.handle);

  // Get primary handle (first available)
  const primaryPlatform = activePlatforms[0];
  const primaryHandle = primaryPlatform
    ? `${primaryPlatform.name}: ${primaryPlatform.handle}`
    : 'No social media connected';

  // Calculate total followers (placeholder - all zeros for now)
  const totalFollowers = activePlatforms.reduce(
    (sum, p) => sum + (p.followers || 0),
    0
  );

  // Format number with commas
  const formatNumber = (num: number) => {
    return num.toLocaleString();
  };

  return (
    <div className="grid grid-cols-1 gap-6 lg:grid-cols-[350px_1fr]">
      {/* Left Column - Profile Info */}
      <div className="space-y-6">
        {/* Photo Card */}
        <Card>
          <CardContent className="flex flex-col items-center py-12">
            <Avatar className="h-32 w-32">
              <AvatarImage src={undefined} alt={roster.name} />
              <AvatarFallback className="text-2xl">
                {roster.name
                  .split(' ')
                  .map((n) => n[0])
                  .join('')
                  .toUpperCase()}
              </AvatarFallback>
            </Avatar>
            <div className="mt-4 text-center">
              <h3 className="text-lg font-semibold">{roster.name}</h3>
              <p className="text-sm text-muted-foreground">{primaryHandle}</p>
            </div>
          </CardContent>
        </Card>

        {/* Bio Card */}
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Bio</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              No bio available. Add a bio field to the roster member to display
              content here.
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Right Column - Social Stats & Highlighted Content */}
      <div className="space-y-6">
        {/* Social Follower Counts Overview */}
        <Card>
          <CardContent className="py-6">
            {/* Platform Breakdown - Now with clickable links */}
            <div className="mb-4 grid grid-cols-2 gap-4 md:grid-cols-4">
              {activePlatforms.map((platform) => (
                <a
                  key={platform.name}
                  href={platform.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex flex-col items-center rounded-lg border p-3 transition-all hover:scale-105 hover:border-primary hover:shadow-md"
                >
                  <div className={platform.color}>{platform.icon}</div>
                  <p className="mt-2 text-xs font-medium">{platform.name}</p>
                  <p className="text-sm text-muted-foreground">
                    {formatNumber(platform.followers || 0)}
                  </p>
                </a>
              ))}
            </div>

            {/* Total Follower Count */}
            <div className="flex items-center justify-center gap-2 rounded-lg bg-muted p-4">
              <Users className="h-5 w-5 text-muted-foreground" />
              <div className="text-center">
                <p className="text-sm font-medium text-muted-foreground">
                  Total Follower Count
                </p>
                <p className="text-2xl font-bold">
                  {formatNumber(totalFollowers)}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Highlighted Content Grid */}
        <div>
          <h3 className="mb-4 text-sm font-medium">Highlighted Content</h3>
          <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
            {[1, 2, 3].map((index) => (
              <Card
                key={index}
                className="aspect-square overflow-hidden border-2 border-dashed"
              >
                <CardContent className="flex h-full items-center justify-center p-6">
                  <p className="text-center text-sm text-muted-foreground">
                    Highlighted
                    <br />
                    Content {index}
                  </p>
                </CardContent>
              </Card>
            ))}
          </div>
          <p className="mt-4 text-center text-xs text-muted-foreground">
            Featured posts, photos, and videos will appear here
          </p>
        </div>
      </div>
    </div>
  );
}
