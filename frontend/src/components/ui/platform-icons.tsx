/**
 * Colorful platform logo components matching official brand colors
 */

interface PlatformIconProps {
  className?: string;
}

export function InstagramIcon({ className = 'h-4 w-4' }: PlatformIconProps) {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
    >
      <defs>
        <radialGradient
          id="instagram-gradient"
          cx="0.3"
          cy="1"
          r="1.2"
          gradientUnits="objectBoundingBox"
        >
          <stop offset="0%" stopColor="#FED576" />
          <stop offset="26%" stopColor="#F47133" />
          <stop offset="60%" stopColor="#BC3081" />
          <stop offset="100%" stopColor="#4C63D2" />
        </radialGradient>
      </defs>
      <rect
        x="2"
        y="2"
        width="20"
        height="20"
        rx="5"
        fill="url(#instagram-gradient)"
      />
      <circle
        cx="12"
        cy="12"
        r="4"
        stroke="white"
        strokeWidth="2"
        fill="none"
      />
      <circle cx="17.5" cy="6.5" r="1.5" fill="white" />
    </svg>
  );
}

export function TikTokIcon({ className = 'h-4 w-4' }: PlatformIconProps) {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
    >
      <rect width="24" height="24" rx="5" fill="black" />
      <path
        d="M16.6 5.82C15.9 5.03 15.5 4 15.5 2.91H12.5V15.5C12.5 16.88 11.38 18 10 18C8.62 18 7.5 16.88 7.5 15.5C7.5 14.12 8.62 13 10 13C10.28 13 10.55 13.05 10.8 13.14V10.09C10.54 10.05 10.27 10.03 10 10.03C6.97 10.03 4.5 12.5 4.5 15.53C4.5 18.56 6.97 21.03 10 21.03C13.03 21.03 15.5 18.56 15.5 15.53V9.7C16.89 10.72 18.6 11.33 20.5 11.33V8.33C18.41 8.33 16.6 7.32 16.6 5.82Z"
        fill="#FF004F"
      />
      <path
        d="M16.6 5.82C15.9 5.03 15.5 4 15.5 2.91H12.5V15.5C12.5 16.88 11.38 18 10 18C8.62 18 7.5 16.88 7.5 15.5C7.5 14.12 8.62 13 10 13C10.28 13 10.55 13.05 10.8 13.14V10.09C10.54 10.05 10.27 10.03 10 10.03C6.97 10.03 4.5 12.5 4.5 15.53C4.5 18.56 6.97 21.03 10 21.03C13.03 21.03 15.5 18.56 15.5 15.53V9.7C16.89 10.72 18.6 11.33 20.5 11.33V8.33C18.41 8.33 16.6 7.32 16.6 5.82Z"
        fill="#00F2EA"
        style={{ mixBlendMode: 'screen' }}
        transform="translate(1, 1)"
      />
    </svg>
  );
}

export function FacebookIcon({ className = 'h-4 w-4' }: PlatformIconProps) {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
    >
      <rect width="24" height="24" rx="5" fill="#1877F2" />
      <path
        d="M16.5 12.75H13.5V21H10.5V12.75H8.25V10.125H10.5V8.25C10.5 6.18 11.79 4.5 14.25 4.5H16.5V7.125H14.85C14.25 7.125 13.5 7.425 13.5 8.475V10.125H16.5V12.75Z"
        fill="white"
      />
    </svg>
  );
}

export function YouTubeIcon({ className = 'h-4 w-4' }: PlatformIconProps) {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
    >
      <rect width="24" height="24" rx="5" fill="#FF0000" />
      <path
        d="M19.615 6.185C19.4 5.4 18.8 4.8 18.015 4.585C16.668 4.2 12 4.2 12 4.2C12 4.2 7.332 4.2 5.985 4.585C5.2 4.8 4.6 5.4 4.385 6.185C4 7.532 4 12 4 12C4 12 4 16.468 4.385 17.815C4.6 18.6 5.2 19.2 5.985 19.415C7.332 19.8 12 19.8 12 19.8C12 19.8 16.668 19.8 18.015 19.415C18.8 19.2 19.4 18.6 19.615 17.815C20 16.468 20 12 20 12C20 12 20 7.532 19.615 6.185Z"
        fill="white"
      />
      <path d="M10 15V9L15 12L10 15Z" fill="#FF0000" />
    </svg>
  );
}
