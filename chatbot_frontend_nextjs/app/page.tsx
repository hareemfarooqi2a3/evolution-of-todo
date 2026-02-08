'use client';

import ChatWidget from '@/components/ChatWidget';

export default function Home() {
  return (
    <main>
      <ChatWidget defaultUserId="test_user" />
    </main>
  );
}
