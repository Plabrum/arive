import { Link } from '@tanstack/react-router';
import { Card } from '@/components/ui/card';
import { Checkbox } from '@/components/ui/checkbox';
import { Image } from '@/components/ui/image';
import {
  InstagramIcon,
  TikTokIcon,
  FacebookIcon,
  YouTubeIcon,
} from '@/components/ui/platform-icons';
import { StateFlag } from '@/components/ui/state-flag';
import { cn } from '@/lib/utils';
import type {
  ObjectListSchema,
  ImageFieldValue,
  ColumnDefinitionSchema,
} from '@/openapi/ariveAPI.schemas';

interface CardViewProps {
  data: ObjectListSchema[];
  columns: ColumnDefinitionSchema[];
  enableRowSelection?: boolean;
  selectedRows: Set<string>;
  onRowSelectionChange: (rowId: string, selected: boolean) => void;
  onRowClick?: (row: ObjectListSchema) => void;
}

// Helper: Extract image field value from ObjectListSchema fields
function getImageFromFields(
  fields: ObjectListSchema['fields']
): ImageFieldValue | null {
  if (!fields) return null;

  for (const field of fields) {
    if (
      field.value &&
      typeof field.value === 'object' &&
      'type' in field.value
    ) {
      if (field.value.type === 'image') {
        return field.value as ImageFieldValue;
      }
    }
  }

  return null;
}

// Helper: Get field value by key
function getFieldValue(row: ObjectListSchema, key: string): string | null {
  const field = row.fields?.find((f) => f.key === key);
  if (!field?.value || typeof field.value !== 'object') return null;
  if ('value' in field.value) {
    const val = field.value.value;
    return typeof val === 'string' ? val : null;
  }
  return null;
}

// Helper: Generate initials from title
function getInitials(title: string): string {
  return title
    .split(' ')
    .map((word) => word[0])
    .join('')
    .toUpperCase()
    .slice(0, 2);
}

// Helper: Generate consistent color from string hash
function getColorFromString(str: string): string {
  const colors = [
    'bg-blue-500',
    'bg-green-500',
    'bg-yellow-500',
    'bg-red-500',
    'bg-purple-500',
    'bg-pink-500',
    'bg-indigo-500',
    'bg-teal-500',
  ];
  const hash = str.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0);
  return colors[hash % colors.length];
}

// Social platform icon mapping with colorful custom icons
const socialIcons = {
  instagram_handle: InstagramIcon,
  facebook_handle: FacebookIcon,
  tiktok_handle: TikTokIcon,
  youtube_channel: YouTubeIcon,
} as const;

// Helper: Calculate age from birthdate
function calculateAge(birthdate: string | null): number | null {
  if (!birthdate) return null;
  try {
    const today = new Date();
    const birth = new Date(birthdate);
    // Check if date is valid
    if (isNaN(birth.getTime())) return null;
    let age = today.getFullYear() - birth.getFullYear();
    const monthDiff = today.getMonth() - birth.getMonth();
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
      age--;
    }
    return age >= 0 ? age : null;
  } catch {
    return null;
  }
}

export function CardView({
  data,
  columns,
  enableRowSelection = false,
  selectedRows,
  onRowSelectionChange,
  onRowClick,
}: CardViewProps) {
  if (!data || data.length === 0) {
    return (
      <div className="text-muted-foreground flex h-64 items-center justify-center">
        <p>No items to display</p>
      </div>
    );
  }

  // Find relevant columns
  const socialColumns = columns.filter((col) =>
    [
      'instagram_handle',
      'facebook_handle',
      'tiktok_handle',
      'youtube_channel',
    ].includes(col.key)
  );

  const birthdateColumn = columns.find((col) => col.key === 'birthdate');
  const genderColumn = columns.find((col) => col.key === 'gender');

  return (
    <div className="w-full">
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
        {data.map((item) => {
          const imageField = getImageFromFields(item.fields);
          const imageUrl = imageField?.thumbnail_url || imageField?.url;
          const isSelected = selectedRows.has(item.id);

          // Extract field values
          const birthdate = birthdateColumn
            ? getFieldValue(item, birthdateColumn.key)
            : null;
          const age = calculateAge(birthdate);
          const gender = genderColumn
            ? getFieldValue(item, genderColumn.key)
            : null;

          // Extract city and state from subtitle (assuming format: "City, State")
          const locationParts = item.subtitle?.split(', ') || [];
          const city = locationParts[0] || null;
          const state = locationParts[1] || null;

          return (
            <Card
              key={item.id}
              className={cn(
                'group relative overflow-hidden transition-all hover:shadow-md',
                isSelected && 'ring-primary ring-2 ring-offset-2'
              )}
            >
              {/* Selection checkbox */}
              {enableRowSelection && (
                <div className="absolute right-2 top-2 z-10">
                  <Checkbox
                    checked={isSelected}
                    onCheckedChange={(checked) =>
                      onRowSelectionChange(item.id, checked === true)
                    }
                    aria-label={`Select ${item.title}`}
                    className="bg-background border-2"
                  />
                </div>
              )}

              {/* Link wrapper for entire card */}
              <Link
                to={item.link || '#'}
                onClick={(e: React.MouseEvent) => {
                  if (onRowClick) {
                    e.preventDefault();
                    onRowClick(item);
                  }
                }}
                className="block p-4"
              >
                {/* Top section: Image on left, Name on right */}
                <div className="flex gap-3">
                  {/* Small image in top-left corner */}
                  <div className="bg-muted relative h-16 w-16 shrink-0 overflow-hidden rounded-md">
                    {imageUrl ? (
                      <Image
                        src={imageUrl}
                        alt={item.title}
                        className="h-full w-full object-cover transition-transform group-hover:scale-105"
                      />
                    ) : (
                      <div
                        className={cn(
                          'flex h-full w-full items-center justify-center',
                          getColorFromString(item.title)
                        )}
                      >
                        <span className="text-lg font-semibold text-white">
                          {getInitials(item.title)}
                        </span>
                      </div>
                    )}
                  </div>

                  {/* Name - middle-aligned, wraps to two lines */}
                  <div className="flex flex-1 items-center">
                    <h3 className="line-clamp-2 text-base font-semibold leading-tight">
                      {item.title}
                    </h3>
                  </div>
                </div>

                {/* Metadata section below */}
                <div className="mt-3 space-y-2">
                  {/* Social handles */}
                  {socialColumns.length > 0 && (
                    <div className="flex flex-col gap-1.5">
                      {socialColumns.map((col) => {
                        const value = getFieldValue(item, col.key);
                        if (!value) return null;

                        const Icon =
                          socialIcons[col.key as keyof typeof socialIcons];

                        return (
                          <div
                            key={col.key}
                            className="flex items-center gap-2"
                          >
                            {Icon && <Icon className="h-4 w-4 shrink-0" />}
                            <span className="text-muted-foreground truncate text-sm">
                              @{value}
                            </span>
                          </div>
                        );
                      })}
                    </div>
                  )}

                  {/* Age */}
                  {age !== null && (
                    <div className="text-muted-foreground text-sm">
                      Age: {age}
                    </div>
                  )}

                  {/* City and State */}
                  {(city || state) && (
                    <div className="flex items-center gap-2">
                      {state && <StateFlag state={state} className="text-muted-foreground h-4 w-4" />}
                      <span className="text-muted-foreground text-sm">
                        {city}
                        {city && state && ', '}
                        {state}
                      </span>
                    </div>
                  )}

                  {/* Gender */}
                  {gender && (
                    <div className="text-muted-foreground text-sm">
                      {gender}
                    </div>
                  )}
                </div>
              </Link>
            </Card>
          );
        })}
      </div>
    </div>
  );
}
