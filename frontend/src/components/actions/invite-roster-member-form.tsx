import { createTypedForm } from '@/components/forms/base';

// Define the schema for invite roster member form
interface InviteRosterMemberSchema {
  email: string;
}

const { FormModal, FormEmail } = createTypedForm<InviteRosterMemberSchema>();

interface InviteRosterMemberFormProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (data: InviteRosterMemberSchema) => void;
  isSubmitting: boolean;
}

/**
 * Form for inviting a roster member via email
 */
export function InviteRosterMemberForm({
  isOpen,
  onClose,
  onSubmit,
  isSubmitting,
}: InviteRosterMemberFormProps) {
  return (
    <FormModal
      isOpen={isOpen}
      onClose={onClose}
      title="Invite Roster Member"
      subTitle="Enter the email address of the person you want to invite to your roster."
      onSubmit={onSubmit}
      isSubmitting={isSubmitting}
      submitText="Send Invitation"
    >
      <FormEmail
        name="email"
        label="Email Address"
        placeholder="user@example.com"
        required="Email is required"
      />
    </FormModal>
  );
}
