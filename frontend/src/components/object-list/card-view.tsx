import { Link } from '@tanstack/react-router';
import {
  InstagramIcon,
  FacebookIcon,
  TikTokIcon,
  YouTubeIcon,
} from '@/components/icons/social-icons';
import { Badge } from '@/components/ui/badge';
import { Card } from '@/components/ui/card';
import { Checkbox } from '@/components/ui/checkbox';
import { Image } from '@/components/ui/image';
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from '@/components/ui/tooltip';
import { formatPhoneNumber } from '@/lib/field-formatters';
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

// Helper: Get number field value by key
function getNumberFieldValue(
  row: ObjectListSchema,
  key: string
): number | null {
  const field = row.fields?.find((f) => f.key === key);
  if (!field?.value || typeof field.value !== 'object') return null;
  if ('value' in field.value) {
    const val = field.value.value;
    return typeof val === 'number' ? val : null;
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

// Social platform icon mapping
const socialIcons = {
  instagram_handle: InstagramIcon,
  facebook_handle: FacebookIcon,
  tiktok_handle: TikTokIcon,
  youtube_channel: YouTubeIcon,
} as const;

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

  // Find contact columns
  const emailColumn = columns.find((col) => col.type === 'email');
  const phoneColumn = columns.find((col) => col.type === 'phone');

  // Find demographic columns
  const cityColumn = columns.find((col) => col.key === 'city');
  const ageColumn = columns.find((col) => col.key === 'age');
  const genderColumn = columns.find((col) => col.key === 'gender');

  // Find social handle columns
  const socialColumns = columns.filter((col) =>
    [
      'instagram_handle',
      'facebook_handle',
      'tiktok_handle',
      'youtube_channel',
    ].includes(col.key)
  );

  return (
    <div className="w-full">
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
        {data.map((item) => {
          const imageField = getImageFromFields(item.fields);
          const imageUrl = imageField?.thumbnail_url || imageField?.url;
          const isSelected = selectedRows.has(item.id);
          const emailValue = emailColumn
            ? getFieldValue(item, emailColumn.key)
            : null;
          const phoneValue = phoneColumn
            ? getFieldValue(item, phoneColumn.key)
            : null;
          const cityValue = cityColumn
            ? getFieldValue(item, cityColumn.key)
            : null;
          const ageValue = ageColumn
            ? getNumberFieldValue(item, ageColumn.key)
            : null;
          const genderValue = genderColumn
            ? getFieldValue(item, genderColumn.key)
            : null;

          return (
            <Card
              key={item.id}
              className={cn(
                'group relative overflow-hidden p-0 transition-all hover:shadow-md',
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
                className="block px-2 pt-2"
              >
                {/* Image or initials */}
                <div className="bg-muted relative aspect-square overflow-hidden rounded-md">
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
                      <span className="text-3xl font-semibold text-white">
                        {getInitials(item.title)}
                      </span>
                    </div>
                  )}
                </div>

                {/* Metadata */}
                <div className="flex flex-col gap-2 p-3">
                  {/* Title and Demographics row */}
                  <div className="flex items-baseline justify-between gap-2">
                    <h3 className="truncate text-base font-semibold leading-tight">
                      {item.title}
                    </h3>
                    {(genderValue || ageValue || cityValue) && (
                      <p className="text-muted-foreground shrink-0 text-xs">
                        {[
                          genderValue,
                          ageValue ? `${ageValue}` : null,
                          cityValue,
                        ]
                          .filter(Boolean)
                          .join(', ')}
                      </p>
                    )}
                  </div>

                  {/* Contact info - Email and Phone as text */}
                  {(emailValue || phoneValue) && (
                    <div className="flex flex-col gap-0.5">
                      {emailValue && (
                        <span className="text-muted-foreground truncate text-xs">
                          {emailValue}
                        </span>
                      )}
                      {phoneValue && (
                        <span className="text-muted-foreground truncate text-xs">
                          {formatPhoneNumber(phoneValue)}
                        </span>
                      )}
                    </div>
                  )}

                  {/* Social media icons with tooltips */}
                  {socialColumns.length > 0 && (
                    <div className="flex items-center gap-2.5">
                      {socialColumns.map((col) => {
                        const value = getFieldValue(item, col.key);
                        if (!value) return null;

                        const Icon =
                          socialIcons[col.key as keyof typeof socialIcons];

                        return Icon ? (
                          <Tooltip key={col.key}>
                            <TooltipTrigger asChild>
                              <button
                                type="button"
                                className="z-10 transition-opacity hover:opacity-80"
                                onClick={(e) => {
                                  e.preventDefault();
                                  e.stopPropagation();
                                }}
                              >
                                <Icon className="h-4 w-4" />
                              </button>
                            </TooltipTrigger>
                            <TooltipContent side="top">
                              <p className="text-xs">{value}</p>
                            </TooltipContent>
                          </Tooltip>
                        ) : (
                          <Badge
                            key={col.key}
                            variant="secondary"
                            className="h-5 gap-0.5 px-1.5 text-[10px]"
                          >
                            <span className="max-w-[60px] truncate">
                              {value}
                            </span>
                          </Badge>
                        );
                      })}
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
