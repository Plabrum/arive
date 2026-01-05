import { Link } from '@tanstack/react-router';
import {
  InstagramIcon,
  FacebookIcon,
  TikTokIcon,
  YouTubeIcon,
} from '@/components/icons/social-icons';
import { Badge } from '@/components/ui/badge';
import { Card } from '@/components/ui/card';
import { Image } from '@/components/ui/image';
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
  isSelectMode?: boolean;
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

// Helper: Capitalize first letter for display
function capitalize(str: string): string {
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
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
  isSelectMode = false,
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
              className="group relative overflow-hidden p-0 transition-all duration-200 hover:-translate-y-1 hover:shadow-lg"
            >
              {/* Selection checkbox - clean circular chip */}
              {enableRowSelection && (
                <div
                  className={cn(
                    'absolute right-3 top-3 z-10 transition-opacity duration-200',
                    // Desktop: show on hover or when selected (always visible if selected)
                    isSelected
                      ? 'opacity-100'
                      : 'opacity-0 group-hover:opacity-100 md:block',
                    // Mobile: show only in select mode
                    isSelected ? '' : 'md:opacity-0',
                    isSelectMode || isSelected
                      ? 'opacity-100'
                      : 'hidden md:block'
                  )}
                >
                  <button
                    type="button"
                    onClick={(e) => {
                      e.preventDefault();
                      e.stopPropagation();
                      onRowSelectionChange(item.id, !isSelected);
                    }}
                    className={cn(
                      'flex h-7 w-7 items-center justify-center rounded-full transition-all duration-200',
                      'border-2 backdrop-blur-md',
                      isSelected
                        ? 'border-white bg-white shadow-md'
                        : 'border-white/50 bg-black/30 hover:scale-110 hover:border-white/80 hover:bg-black/50'
                    )}
                    aria-label={`Select ${item.title}`}
                  >
                    {isSelected && (
                      <svg
                        viewBox="0 0 14 14"
                        fill="none"
                        className="h-3.5 w-3.5"
                      >
                        <path
                          d="M2 7L5.5 10.5L12 3.5"
                          stroke="black"
                          strokeWidth="2"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                        />
                      </svg>
                    )}
                  </button>
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
                      className="h-full w-full object-cover"
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
                          genderValue ? capitalize(genderValue) : null,
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

                  {/* Social media icons with expandable handles */}
                  {socialColumns.length > 0 && (
                    <div className="flex items-center gap-2.5">
                      {socialColumns.map((col) => {
                        const value = getFieldValue(item, col.key);
                        if (!value) return null;

                        const Icon =
                          socialIcons[col.key as keyof typeof socialIcons];

                        return Icon ? (
                          <div
                            key={col.key}
                            className="group/social flex items-center gap-1.5 overflow-hidden"
                          >
                            <Icon className="h-4 w-4 shrink-0" />
                            <span className="text-muted-foreground max-w-0 truncate text-xs transition-all duration-200 group-hover/social:max-w-[100px]">
                              {value}
                            </span>
                          </div>
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
