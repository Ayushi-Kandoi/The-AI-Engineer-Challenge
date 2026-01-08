'use client';

import { useState, useEffect } from 'react';
import { checkHealth, sendChatMessage } from '@/lib/api';
import styles from './page.module.css';

export default function Home() {
  const [message, setMessage] = useState('');
  const [reply, setReply] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isCheckingHealth, setIsCheckingHealth] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [healthStatus, setHealthStatus] = useState<string | null>(null);

  // Check backend health on component mount
  useEffect(() => {
    const verifyBackend = async () => {
      try {
        setIsCheckingHealth(true);
        const health = await checkHealth();
        setHealthStatus(health.status);
        setError(null);
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : 'Failed to connect to backend. Make sure the FastAPI server is running at http://127.0.0.1:8000'
        );
        setHealthStatus(null);
      } finally {
        setIsCheckingHealth(false);
      }
    };

    verifyBackend();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!message.trim()) {
      setError('Please enter a message');
      return;
    }

    setIsLoading(true);
    setError(null);
    setReply(null);

    try {
      const response = await sendChatMessage(message);
      setReply(response.reply);
      setMessage('');
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'Failed to send message. Please try again.'
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className={styles.main}>
      <div className={styles.container}>
        <div className={styles.header}>
          <h1 className={styles.title}>Mental Coach</h1>
          <p className={styles.subtitle}>
            Your supportive AI companion for stress, motivation, habits, and confidence
          </p>
        </div>

        {/* Health Status Indicator */}
        {isCheckingHealth ? (
          <div className={styles.card}>
            <div className={styles.loadingState}>
              <div className={styles.loadingSpinner}></div>
              <span style={{ marginLeft: '0.5rem' }}>Checking backend connection...</span>
            </div>
          </div>
        ) : healthStatus ? (
          <div className={styles.successMessage}>
            ✓ Backend connected successfully
          </div>
        ) : null}

        {/* Error Display */}
        {error && (
          <div className={styles.errorMessage}>
            <strong>Error:</strong> {error}
            {error.includes('quota') && (
              <div style={{ marginTop: '0.5rem', fontSize: '0.9rem' }}>
                💡 <strong>Tip:</strong> You may need to add billing information or upgrade your OpenAI plan to continue using the API.
              </div>
            )}
          </div>
        )}

        {/* Chat Interface */}
        <div className={styles.card}>
          <form onSubmit={handleSubmit} className={styles.chatForm}>
            <div className={styles.inputGroup}>
              <label htmlFor="message" className={styles.label}>
                Your Message
              </label>
              <textarea
                id="message"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder="Share what's on your mind..."
                className={styles.textarea}
                rows={4}
                disabled={isLoading || isCheckingHealth}
              />
            </div>
            <button
              type="submit"
              className={`${styles.button} ${styles.buttonPrimary}`}
              disabled={isLoading || isCheckingHealth || !message.trim()}
            >
              {isLoading ? (
                <>
                  <div className={styles.loadingSpinner}></div>
                  <span style={{ marginLeft: '0.5rem' }}>Sending...</span>
                </>
              ) : (
                'Send Message'
              )}
            </button>
          </form>
        </div>

        {/* Reply Display */}
        {reply && (
          <div className={styles.card}>
            <h2 className={styles.replyTitle}>Coach&apos;s Response</h2>
            <div className={styles.replyContent}>{reply}</div>
          </div>
        )}

        {/* Info Card */}
        <div className={styles.card}>
          <h2 className={styles.infoTitle}>About</h2>
          <p className={styles.infoText}>
            This application connects to a FastAPI backend running at{' '}
            <code className={styles.code}>
              {process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000'}
            </code>
            . The backend uses OpenAI&apos;s GPT-5 model to provide supportive mental coaching.
          </p>
        </div>
      </div>
    </main>
  );
}
