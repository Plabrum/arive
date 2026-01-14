import { useState } from 'react';
import { InviteRosterMemberForm } from '@/components/actions/invite-roster-member-form';
import { ObjectList, TopLevelActions } from '@/components/object-list';
import { PageTopBar } from '@/components/page-topbar';
import { Button } from '@/components/ui/button';
import { ActionGroupType } from '@/openapi/ariveAPI.schemas';
import { toast } from 'sonner';

export function RosterPage() {
  const [currentViewId, setCurrentViewId] = useState<unknown | null>(null);
  const [isInviteDialogOpen, setIsInviteDialogOpen] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleInviteSubmit = async (data: { email: string }) => {
    setIsSubmitting(true);
    try {
      // TODO: Implement actual invite API call
      console.log('Inviting roster member:', data.email);

      // Simulate API call
      await new Promise((resolve) => setTimeout(resolve, 1000));

      toast.success(`Invitation sent to ${data.email}`);
      setIsInviteDialogOpen(false);
    } catch (error) {
      toast.error('Failed to send invitation');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <PageTopBar
      title="Roster"
      actions={
        <TopLevelActions actionGroup={ActionGroupType.roster_actions}>
          <Button
            variant="outline"
            size="sm"
            onClick={() => setIsInviteDialogOpen(true)}
          >
            Invite Roster Member
          </Button>
        </TopLevelActions>
      }
    >
      <ObjectList
        objectType="roster"
        currentViewId={currentViewId}
        onViewSelect={setCurrentViewId}
      />

      <InviteRosterMemberForm
        isOpen={isInviteDialogOpen}
        onClose={() => setIsInviteDialogOpen(false)}
        onSubmit={handleInviteSubmit}
        isSubmitting={isSubmitting}
      />
    </PageTopBar>
  );
}
