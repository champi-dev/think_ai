import { useState } from 'react';
import { useStore } from '../../store/store';
import { conversations as conversationsApi } from '../../utils/api';
import { MessageSquare, Trash2, Edit2 } from 'lucide-react';

export default function ConversationItem({ conversation, isActive }) {
  const { setCurrentConversation, updateConversation, deleteConversation } = useStore();
  const [isEditing, setIsEditing] = useState(false);
  const [title, setTitle] = useState(conversation.title);
  const [showActions, setShowActions] = useState(false);

  const handleClick = () => {
    if (!isEditing) {
      setCurrentConversation(conversation);
    }
  };

  const handleEdit = (e) => {
    e.stopPropagation();
    setIsEditing(true);
  };

  const handleSave = async () => {
    if (title.trim() && title !== conversation.title) {
      try {
        await conversationsApi.update(conversation.id, { title: title.trim() });
        updateConversation(conversation.id, { title: title.trim() });
      } catch (error) {
        console.error('Failed to update conversation:', error);
        setTitle(conversation.title);
      }
    }
    setIsEditing(false);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      handleSave();
    } else if (e.key === 'Escape') {
      setTitle(conversation.title);
      setIsEditing(false);
    }
  };

  const handleDelete = async (e) => {
    e.stopPropagation();
    if (confirm('Are you sure you want to delete this conversation?')) {
      try {
        await conversationsApi.delete(conversation.id);
        deleteConversation(conversation.id);
      } catch (error) {
        console.error('Failed to delete conversation:', error);
      }
    }
  };

  return (
    <div
      className={`group relative mb-1 rounded-lg transition-all cursor-pointer ${
        isActive
          ? 'bg-bg-active border-l-2 border-primary pl-3'
          : 'hover:bg-bg-hover pl-3.5'
      }`}
      onClick={handleClick}
      onMouseEnter={() => setShowActions(true)}
      onMouseLeave={() => setShowActions(false)}
    >
      <div className="flex items-center gap-3 py-3 pr-3">
        <MessageSquare
          size={16}
          className={isActive ? 'text-primary' : 'text-text-secondary'}
        />

        {isEditing ? (
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            onBlur={handleSave}
            onKeyDown={handleKeyDown}
            className="flex-1 bg-bg-tertiary border border-border-primary rounded px-2 py-1 text-sm text-text-primary focus:outline-none focus:border-primary"
            autoFocus
            onClick={(e) => e.stopPropagation()}
          />
        ) : (
          <span className="flex-1 text-sm text-text-primary truncate">
            {conversation.title}
          </span>
        )}

        {showActions && !isEditing && (
          <div className="flex items-center gap-1" onClick={(e) => e.stopPropagation()}>
            <button
              onClick={handleEdit}
              className="p-1 rounded hover:bg-bg-tertiary transition-colors"
              title="Rename"
            >
              <Edit2 size={14} className="text-text-tertiary hover:text-text-primary" />
            </button>
            <button
              onClick={handleDelete}
              className="p-1 rounded hover:bg-bg-tertiary transition-colors"
              title="Delete"
            >
              <Trash2 size={14} className="text-text-tertiary hover:text-red-500" />
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
