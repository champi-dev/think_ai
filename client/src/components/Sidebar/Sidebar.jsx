import { useEffect } from 'react';
import { useStore } from '../../store/store';
import { conversations as conversationsApi, auth } from '../../utils/api';
import ConversationItem from './ConversationItem';
import { Plus, LogOut, Brain, Menu, X } from 'lucide-react';
import Button from '../Common/Button';

export default function Sidebar() {
  const {
    conversations,
    setConversations,
    currentConversation,
    setCurrentConversation,
    addConversation,
    isSidebarOpen,
    toggleSidebar,
    user,
    logout,
  } = useStore();

  useEffect(() => {
    loadConversations();
  }, []);

  const loadConversations = async () => {
    try {
      const response = await conversationsApi.getAll();
      setConversations(response.data.data);
    } catch (error) {
      console.error('Failed to load conversations:', error);
    }
  };

  const handleNewConversation = async () => {
    try {
      const response = await conversationsApi.create({ title: 'New Chat' });
      const newConv = response.data.data;
      addConversation(newConv);
      setCurrentConversation(newConv);
    } catch (error) {
      console.error('Failed to create conversation:', error);
    }
  };

  const handleLogout = async () => {
    try {
      await auth.logout();
      logout();
      window.location.href = '/login';
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  const groupedConversations = {
    today: [],
    yesterday: [],
    week: [],
    older: [],
  };

  const now = new Date();
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  const yesterday = new Date(today);
  yesterday.setDate(yesterday.getDate() - 1);
  const weekAgo = new Date(today);
  weekAgo.setDate(weekAgo.getDate() - 7);

  conversations.forEach((conv) => {
    const convDate = new Date(conv.updated_at);
    if (convDate >= today) {
      groupedConversations.today.push(conv);
    } else if (convDate >= yesterday) {
      groupedConversations.yesterday.push(conv);
    } else if (convDate >= weekAgo) {
      groupedConversations.week.push(conv);
    } else {
      groupedConversations.older.push(conv);
    }
  });

  return (
    <>
      {/* Mobile toggle button */}
      <button
        onClick={toggleSidebar}
        className="lg:hidden fixed top-4 right-4 z-50 w-10 h-10 sm:w-12 sm:h-12 bg-bg-tertiary border border-border-primary rounded-lg flex items-center justify-center hover:bg-bg-hover transition-colors shadow-lg"
      >
        {isSidebarOpen ? <X size={20} className="sm:w-6 sm:h-6" /> : <Menu size={20} className="sm:w-6 sm:h-6" />}
      </button>

      {/* Overlay for mobile */}
      {isSidebarOpen && (
        <div
          className="lg:hidden fixed inset-0 bg-black/50 z-40"
          onClick={toggleSidebar}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`fixed lg:static inset-y-0 left-0 z-40 w-[280px] sm:w-80 lg:w-[320px] 2xl:w-[400px] bg-bg-secondary/70 backdrop-blur-xl border-r border-border-primary flex flex-col transition-transform duration-300 ${
          isSidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        }`}
      >
        {/* Header */}
        <div className="p-3 sm:p-4 lg:p-5 2xl:p-6 border-b border-border-primary flex items-center justify-between">
          <div className="flex items-center gap-2 sm:gap-3 lg:gap-4">
            <div className="w-7 h-7 sm:w-8 sm:h-8 lg:w-10 lg:h-10 2xl:w-12 2xl:h-12 bg-gradient-to-br from-primary to-accent-1 rounded-lg flex items-center justify-center">
              <Brain className="w-4 h-4 sm:w-5 sm:h-5 lg:w-6 lg:h-6 2xl:w-7 2xl:h-7 text-white" />
            </div>
            <h1 className="text-lg sm:text-xl lg:text-2xl 2xl:text-3xl font-semibold">Think AI</h1>
          </div>
        </div>

        {/* New Chat Button */}
        <div className="p-3 sm:p-4 lg:p-5 2xl:p-6">
          <Button
            onClick={handleNewConversation}
            variant="primary"
            className="w-full flex items-center justify-center gap-2 text-sm sm:text-base lg:text-lg 2xl:text-xl py-2.5 sm:py-3 lg:py-4"
          >
            <Plus size={16} className="sm:w-5 sm:h-5 lg:w-6 lg:h-6 2xl:w-7 2xl:h-7" />
            New Chat
          </Button>
        </div>

        {/* Conversations List */}
        <div className="flex-1 overflow-y-auto px-2 sm:px-3 lg:px-4">
          {groupedConversations.today.length > 0 && (
            <div className="mb-3 sm:mb-4">
              <h3 className="text-xs sm:text-xs lg:text-sm 2xl:text-base font-semibold text-text-tertiary uppercase tracking-wider px-2 sm:px-3 mb-1.5 sm:mb-2">
                Today
              </h3>
              {groupedConversations.today.map((conv) => (
                <ConversationItem
                  key={conv.id}
                  conversation={conv}
                  isActive={currentConversation?.id === conv.id}
                />
              ))}
            </div>
          )}

          {groupedConversations.yesterday.length > 0 && (
            <div className="mb-3 sm:mb-4">
              <h3 className="text-xs sm:text-xs lg:text-sm 2xl:text-base font-semibold text-text-tertiary uppercase tracking-wider px-2 sm:px-3 mb-1.5 sm:mb-2">
                Yesterday
              </h3>
              {groupedConversations.yesterday.map((conv) => (
                <ConversationItem
                  key={conv.id}
                  conversation={conv}
                  isActive={currentConversation?.id === conv.id}
                />
              ))}
            </div>
          )}

          {groupedConversations.week.length > 0 && (
            <div className="mb-3 sm:mb-4">
              <h3 className="text-xs sm:text-xs lg:text-sm 2xl:text-base font-semibold text-text-tertiary uppercase tracking-wider px-2 sm:px-3 mb-1.5 sm:mb-2">
                Previous 7 Days
              </h3>
              {groupedConversations.week.map((conv) => (
                <ConversationItem
                  key={conv.id}
                  conversation={conv}
                  isActive={currentConversation?.id === conv.id}
                />
              ))}
            </div>
          )}

          {groupedConversations.older.length > 0 && (
            <div className="mb-3 sm:mb-4">
              <h3 className="text-xs sm:text-xs lg:text-sm 2xl:text-base font-semibold text-text-tertiary uppercase tracking-wider px-2 sm:px-3 mb-1.5 sm:mb-2">
                Older
              </h3>
              {groupedConversations.older.map((conv) => (
                <ConversationItem
                  key={conv.id}
                  conversation={conv}
                  isActive={currentConversation?.id === conv.id}
                />
              ))}
            </div>
          )}

          {conversations.length === 0 && (
            <div className="text-center py-6 sm:py-8 text-text-tertiary text-xs sm:text-sm lg:text-base px-4">
              No conversations yet. Start a new chat!
            </div>
          )}
        </div>

        {/* User Profile */}
        <div className="p-3 sm:p-4 lg:p-5 2xl:p-6 border-t border-border-primary">
          <div className="flex items-center gap-2 sm:gap-3 mb-2 sm:mb-3">
            <div className="w-8 h-8 sm:w-10 sm:h-10 lg:w-12 lg:h-12 2xl:w-14 2xl:h-14 bg-gradient-to-br from-primary to-accent-1 rounded-full flex items-center justify-center">
              <span className="text-white font-semibold text-sm sm:text-base lg:text-lg 2xl:text-xl">
                {user?.username?.[0]?.toUpperCase() || 'U'}
              </span>
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-xs sm:text-sm lg:text-base 2xl:text-lg font-medium text-text-primary truncate">
                {user?.username || 'User'}
              </p>
              <p className="text-xs sm:text-xs lg:text-sm 2xl:text-base text-text-tertiary truncate">
                {user?.email || ''}
              </p>
            </div>
          </div>
          <div className="flex gap-2">
            <Button
              variant="ghost"
              size="sm"
              className="flex-1 flex items-center gap-2 text-xs sm:text-sm lg:text-base 2xl:text-lg py-2 sm:py-2.5 lg:py-3"
              onClick={handleLogout}
            >
              <LogOut size={14} className="sm:w-4 sm:h-4 lg:w-5 lg:h-5 2xl:w-6 2xl:h-6" />
              <span>Log Out</span>
            </Button>
          </div>
        </div>
      </aside>
    </>
  );
}
