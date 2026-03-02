import { createTypedForm } from '@/components/forms/base';
import { CollapsibleFormSection } from '@/components/ui/collapsible-form-section';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Checkbox } from '@/components/ui/checkbox';
import type { RosterCreateSchema } from '@/openapi/ariveAPI.schemas';
import { useState } from 'react';

const {
  FormModal,
  FormString,
  FormEmail,
  FormDatetime,
  FormImageUpload,
  FormCustom,
  FormAddress,
} = createTypedForm<RosterCreateSchema>();

interface CreateRosterFormProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (data: RosterCreateSchema) => void;
  isSubmitting: boolean;
  actionLabel: string;
}

const GENDER_OPTIONS = [
  { value: 'male', label: 'Male' },
  { value: 'female', label: 'Female' },
  { value: 'other', label: 'Other' },
];

/**
 * Form for creating a new roster member (talent/influencer)
 */
export function CreateRosterForm({
  isOpen,
  onClose,
  onSubmit,
  isSubmitting,
  actionLabel,
}: CreateRosterFormProps) {
  const [sameAsMailing, setSameAsMailing] = useState(false);

  return (
    <FormModal
      isOpen={isOpen}
      onClose={onClose}
      title={actionLabel}
      subTitle="Fill out the form below to create a new roster member."
      onSubmit={(data) => {
        // If "same as mailing" is checked, copy mailing_address to address
        if (sameAsMailing) {
          data.address = data.mailing_address;
        }
        onSubmit(data);
      }}
      isSubmitting={isSubmitting}
      submitText="Create Roster Member"
    >
      {/* Basic Information */}
      <FormString
        name="name"
        label="Name"
        placeholder="Talent name"
        required="Name is required"
        autoFocus
      />

      <FormEmail name="email" label="Email" placeholder="email@example.com" />

      <FormString name="phone" label="Phone" placeholder="+1 (555) 000-0000" />

      {/* Additional Options - Collapsible */}
      <CollapsibleFormSection title="Additional options" defaultOpen={false}>
        {/* Social Media Section */}
        <div className="space-y-4 rounded-lg border p-4">
          <h4 className="text-sm font-medium">Social Media</h4>

          <FormString
            name="instagram_handle"
            label="Instagram Handle"
            placeholder="@username"
          />

          <FormString
            name="facebook_handle"
            label="Facebook Handle"
            placeholder="@username"
          />

          <FormString
            name="tiktok_handle"
            label="TikTok Handle"
            placeholder="@username"
          />

          <FormString
            name="youtube_channel"
            label="YouTube Channel"
            placeholder="Channel name or URL"
          />
        </div>

        {/* Profile Photo Section */}
        <FormImageUpload
          name="profile_photo_id"
          label="Profile Photo"
          description="JPG, PNG, or GIF (max 10MB)"
        />

        {/* Address Section */}
        <div className="space-y-4">
          {/* Mailing Address (first) */}
          <FormAddress name="mailing_address" label="Mailing Address" />

          {/* Home Address (second, with checkbox) */}
          <div className="space-y-3">
            <div className="flex items-center space-x-2">
              <Checkbox
                id="same-as-mailing"
                checked={sameAsMailing}
                onCheckedChange={(checked) => setSameAsMailing(checked === true)}
              />
              <label
                htmlFor="same-as-mailing"
                className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
              >
                Same as mailing address
              </label>
            </div>

            {!sameAsMailing && <FormAddress name="address" label="Home Address" />}
          </div>
        </div>

        {/* Birthday & Gender Section */}
        <div className="space-y-4 rounded-lg border p-4">
          <h4 className="text-sm font-medium">Personal Information</h4>

          <FormDatetime
            name="birthdate"
            label="Birthday"
            placeholder="Select date"
          />

          <FormCustom name="gender">
            {({ value, onChange }) => {
              // Determine if we should show the "other" text field
              // Show it if value is anything other than 'male' or 'female'
              const showOtherField =
                value !== 'male' &&
                value !== 'female' &&
                value !== undefined &&
                value !== null &&
                value !== '';
              const selectValue = showOtherField
                ? 'other'
                : (value as string) || '';

              return (
                <div className="space-y-3">
                  <div>
                    <Label htmlFor="gender-select">Gender</Label>
                    <Select
                      value={selectValue}
                      onValueChange={(newValue) => {
                        if (newValue === 'other') {
                          // Set to empty string to show the text input with empty value
                          onChange('');
                        } else {
                          onChange(newValue);
                        }
                      }}
                    >
                      <SelectTrigger id="gender-select" className="mt-1">
                        <SelectValue placeholder="Select gender (optional)" />
                      </SelectTrigger>
                      <SelectContent>
                        {GENDER_OPTIONS.map((option) => (
                          <SelectItem key={option.value} value={option.value}>
                            {option.label}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                  {selectValue === 'other' && (
                    <div>
                      <Label htmlFor="gender-custom">Please specify</Label>
                      <Input
                        id="gender-custom"
                        type="text"
                        placeholder="Enter gender identity"
                        value={(value as string) || ''}
                        onChange={(e) => onChange(e.target.value)}
                        className="mt-1"
                        autoFocus
                      />
                    </div>
                  )}
                </div>
              );
            }}
          </FormCustom>
        </div>
      </CollapsibleFormSection>
    </FormModal>
  );
}
