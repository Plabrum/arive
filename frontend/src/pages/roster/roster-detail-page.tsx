import { useParams } from '@tanstack/react-router';
import { ObjectActions } from '@/components/object-detail';
import { ObjectDetailTabs } from '@/components/object-detail-tabs';
import { PageTopBar } from '@/components/page-topbar';
import { CreatorDetailsLayout } from '@/components/roster-detail';
import { TabsContent } from '@/components/ui/tabs';
import { ActionGroupType } from '@/openapi/ariveAPI.schemas';
import { useRosterIdGetRosterSuspense } from '@/openapi/roster/roster';

export function RosterDetailPage() {
  const { id } = useParams({ from: '/_authenticated/roster/$id' });
  const { data, refetch } = useRosterIdGetRosterSuspense(id);

  return (
    <PageTopBar
      title={data.name}
      state={data.state}
      actions={
        <ObjectActions
          data={data}
          actionGroup={ActionGroupType.roster_actions}
          onRefetch={refetch}
        />
      }
    >
      <ObjectDetailTabs
        tabs={[{ value: 'summary', label: 'Creator Details' }]}
        defaultTab="summary"
      >
        <TabsContent value="summary" className="space-y-6">
          <CreatorDetailsLayout roster={data} />
        </TabsContent>
      </ObjectDetailTabs>
    </PageTopBar>
  );
}
