import { Instagram, Facebook, Youtube, ExternalLink } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { cn } from '@/lib/utils';
import type { RosterSchema } from '@/openapi/ariveAPI.schemas';

interface RosterMediaKitProps {
  roster: RosterSchema;
}

interface SocialPlatform {
  name: string;
  handle: string | null | undefined;
  url: string;
  icon: React.ReactNode;
  gradient: string;
  textColor: string;
}

export function RosterMediaKit({ roster }: RosterMediaKitProps) {
  // Build array of social platforms with their data
  const platforms: SocialPlatform[] = [
    {
      name: 'Instagram',
      handle: roster.instagram_handle,
      url: roster.instagram_handle
        ? `https://instagram.com/${roster.instagram_handle.replace('@', '')}`
        : '',
      icon: <Instagram className="h-12 w-12" />,
      gradient: 'from-purple-500 via-pink-500 to-orange-500',
      textColor: 'text-white',
    },
    {
      name: 'TikTok',
      handle: roster.tiktok_handle,
      url: roster.tiktok_handle
        ? `https://tiktok.com/@${roster.tiktok_handle.replace('@', '')}`
        : '',
      icon: (
        <svg
          className="h-12 w-12"
          viewBox="0 0 24 24"
          fill="currentColor"
        >
          <path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-5.2 1.74 2.89 2.89 0 0 1 2.31-4.64 2.93 2.93 0 0 1 .88.13V9.4a6.84 6.84 0 0 0-1-.05A6.33 6.33 0 0 0 5 20.1a6.34 6.34 0 0 0 10.86-4.43v-7a8.16 8.16 0 0 0 4.77 1.52v-3.4a4.85 4.85 0 0 1-1-.1z" />
        </svg>
      ),
      gradient: 'from-black via-gray-900 to-black',
      textColor: 'text-white',
    },
    {
      name: 'YouTube',
      handle: roster.youtube_channel,
      url: roster.youtube_channel || '',
      icon: <Youtube className="h-12 w-12" />,
      gradient: 'from-red-600 via-red-500 to-red-600',
      textColor: 'text-white',
    },
    {
      name: 'Facebook',
      handle: roster.facebook_handle,
      url: roster.facebook_handle
        ? `https://facebook.com/${roster.facebook_handle}`
        : '',
      icon: <Facebook className="h-12 w-12" />,
      gradient: 'from-blue-600 via-blue-500 to-blue-700',
      textColor: 'text-white',
    },
  ];

  // Filter to only platforms with handles
  const activePlatforms = platforms.filter((p) => p.handle);

  if (activePlatforms.length === 0) {
    return (
      <div className="flex min-h-[400px] items-center justify-center">
        <Card className="w-full max-w-md">
          <CardContent className="flex flex-col items-center justify-center py-12 text-center">
            <div className="mb-4 rounded-full bg-muted p-4">
              <ExternalLink className="h-8 w-8 text-muted-foreground" />
            </div>
            <h3 className="mb-2 text-lg font-semibold">No Social Media Connected</h3>
            <p className="text-sm text-muted-foreground">
              Add social media handles to {roster.name}'s profile to display them here.
            </p>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Hero Section */}
      <div className="relative overflow-hidden rounded-xl bg-gradient-to-br from-neutral-900 via-neutral-800 to-neutral-900 p-8 text-white">
        <div className="relative z-10 space-y-4">
          <h2 className="text-3xl font-bold tracking-tight">Media Kit</h2>
          <p className="text-lg text-neutral-300">
            Connect with {roster.name} across social media
          </p>
        </div>
        {/* Decorative gradient overlay */}
        <div className="absolute right-0 top-0 h-full w-1/2 bg-gradient-to-l from-purple-500/10 to-transparent" />
      </div>

      {/* Social Platform Grid */}
      <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
        {activePlatforms.map((platform) => (
          <a
            key={platform.name}
            href={platform.url}
            target="_blank"
            rel="noopener noreferrer"
            className="group block transition-transform hover:scale-[1.02]"
          >
            <Card className="overflow-hidden border-2 transition-all hover:border-primary hover:shadow-lg">
              <div
                className={cn(
                  'flex h-48 flex-col items-center justify-center bg-gradient-to-br p-8',
                  platform.gradient,
                  platform.textColor
                )}
              >
                <div className="mb-4 transition-transform group-hover:scale-110">
                  {platform.icon}
                </div>
                <h3 className="text-xl font-bold">{platform.name}</h3>
                <p className="mt-2 text-sm opacity-90">{platform.handle}</p>
              </div>
              <CardContent className="flex items-center justify-between p-4">
                <span className="text-sm font-medium text-muted-foreground">
                  View Profile
                </span>
                <ExternalLink className="h-4 w-4 text-muted-foreground transition-transform group-hover:translate-x-1" />
              </CardContent>
            </Card>
          </a>
        ))}
      </div>

      {/* Highlighted Content Section - Placeholder for future media */}
      <div className="rounded-xl border-2 border-dashed border-muted p-12 text-center">
        <h3 className="mb-2 text-lg font-semibold text-muted-foreground">
          Highlighted Media
        </h3>
        <p className="text-sm text-muted-foreground">
          Featured posts, photos, and videos will appear here
        </p>
      </div>
    </div>
  );
}
