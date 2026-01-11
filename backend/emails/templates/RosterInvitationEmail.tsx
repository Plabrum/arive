import { Heading, Section, Text } from "@react-email/components";
import * as React from "react";
import { BaseLayout, Button } from "./components";

interface RosterInvitationEmailProps {
  roster_name: string;
  inviter_name: string;
  invitation_url: string;
  expiration_hours: string | number;
}

export default function RosterInvitationEmail({
  roster_name = "Alex Johnson",
  inviter_name = "Sarah Smith",
  invitation_url = "https://tryarive.com/accept-invitation?token=abc123",
  expiration_hours = 72,
}: RosterInvitationEmailProps) {
  return (
    <BaseLayout
      preview={`${inviter_name} invited you to access your campaign portal on Arive`}
    >
      <Section className="mb-6">
        <Heading className="text-foreground text-[28px] font-bold m-0 leading-tight tracking-tight">
          You've been invited to your campaign portal
        </Heading>
      </Section>

      <Text className="text-muted-foreground text-base leading-relaxed mb-4 font-normal">
        Hi {roster_name},
      </Text>

      <Text className="text-muted-foreground text-base leading-relaxed mb-8 font-normal">
        <strong className="text-foreground font-semibold">
          {inviter_name}
        </strong>{" "}
        has invited you to access your campaign portal on Arive. You'll be able
        to view your campaigns, upload content, and track deliverables.
      </Text>

      <Section className="my-8 text-center">
        <Button href={invitation_url}>Accept Invitation</Button>
      </Section>

      {/* Alternative link section */}
      <Section className="mt-12 mb-8">
        <Text className="text-[13px] text-neutral-400 mb-2 font-medium uppercase tracking-wider m-0">
          Or copy this link:
        </Text>
        <div className="bg-neutral-50 border border-border rounded-lg p-4">
          <Text className="text-muted-foreground text-[13px] break-all m-0 leading-normal font-mono">
            {invitation_url}
          </Text>
        </div>
      </Section>

      {/* Security notice */}
      <Section className="mt-12 p-4 bg-neutral-50 rounded-lg border border-neutral-100">
        <Text className="text-muted-foreground text-sm leading-relaxed m-0">
          <strong className="text-foreground font-semibold">
            Didn't expect this invitation?
          </strong>
          <br />
          This invitation will expire in {expiration_hours} hours. If you didn't
          request this, you can safely ignore this email.
        </Text>
      </Section>
    </BaseLayout>
  );
}
