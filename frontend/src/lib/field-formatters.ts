/**
 * Field value formatters for different field types.
 * These formatters handle display formatting based on backend field types.
 */

/**
 * Format a phone number for display.
 * Handles US phone numbers with and without country codes.
 */
export function formatPhoneNumber(phone: string): string {
  // Remove all non-numeric characters
  const cleaned = phone.replace(/\D/g, '');

  // Format as (XXX) XXX-XXXX for 10-digit US numbers
  if (cleaned.length === 10) {
    return `(${cleaned.slice(0, 3)}) ${cleaned.slice(3, 6)}-${cleaned.slice(6)}`;
  }

  // Format as +1 (XXX) XXX-XXXX for 11-digit numbers (with country code)
  if (cleaned.length === 11 && cleaned[0] === '1') {
    return `+1 (${cleaned.slice(1, 4)}) ${cleaned.slice(4, 7)}-${cleaned.slice(7)}`;
  }

  // Return original if it doesn't match expected formats
  return phone;
}

/**
 * Format a field value based on its type.
 * This can be extended to handle other field types as needed.
 */
export function formatFieldValue(value: string, type: string): string {
  switch (type) {
    case 'phone':
      return formatPhoneNumber(value);
    case 'email':
      return value.toLowerCase();
    default:
      return value;
  }
}
