import { FaInstagram, FaFacebook, FaTiktok, FaYoutube } from 'react-icons/fa6';
import type { IconBaseProps } from 'react-icons';

/**
 * Colored social media icons using react-icons with official brand colors.
 * These icons use filled styles for better visual impact and brand recognition.
 */

export function InstagramIcon({ className, ...props }: IconBaseProps) {
  return (
    <FaInstagram
      className={className}
      style={{ color: '#E4405F' }} // Instagram brand color
      {...props}
    />
  );
}

export function FacebookIcon({ className, ...props }: IconBaseProps) {
  return (
    <FaFacebook
      className={className}
      style={{ color: '#1877F2' }} // Facebook brand color
      {...props}
    />
  );
}

export function TikTokIcon({ className, ...props }: IconBaseProps) {
  return (
    <FaTiktok
      className={className}
      style={{ color: '#000000' }} // TikTok brand color (black)
      {...props}
    />
  );
}

export function YouTubeIcon({ className, ...props }: IconBaseProps) {
  return (
    <FaYoutube
      className={className}
      style={{ color: '#FF0000' }} // YouTube brand color
      {...props}
    />
  );
}
