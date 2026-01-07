import { useState } from 'react';
import { ObjectList, TopLevelActions } from '@/components/object-list';
import { PageTopBar } from '@/components/page-topbar';
import { Button } from '@/components/ui/button';
import { ActionGroupType } from '@/openapi/ariveAPI.schemas';

export function RosterPage() {
  const [currentViewId, setCurrentViewId] = useState<unknown | null>(null);

  return (
    <PageTopBar
      title="Roster"
      actions={
        <TopLevelActions actionGroup={ActionGroupType.roster_actions}>
          <Button
            variant="outline"
            size="sm"
            onClick={() => {
              // TODO: Implement invite roster member functionality
              console.log('Invite roster member clicked');
            }}
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
    </PageTopBar>
  );
}
