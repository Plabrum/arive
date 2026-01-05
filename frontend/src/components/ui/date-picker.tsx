'use client';

import * as React from 'react';
import { format } from 'date-fns';
import { CalendarIcon } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Calendar } from '@/components/ui/calendar';
import { Input } from '@/components/ui/input';
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover';
import { cn } from '@/lib/utils';

function formatDate(date: Date | undefined) {
  if (!date) {
    return '';
  }

  return format(date, 'PPP'); // e.g., "January 15, 2025"
}

function isValidDate(date: Date | undefined) {
  if (!date) {
    return false;
  }
  return !isNaN(date.getTime());
}

export interface DatePickerProps {
  id?: string;
  value?: Date;
  onChange?: (date: Date | undefined) => void;
  placeholder?: string;
  disabled?: boolean;
  className?: string;
  fromYear?: number;
  toYear?: number;
}

/**
 * Stock shadcn date picker component with input support
 * Based on: https://ui.shadcn.com/docs/components/date-picker
 */
export function DatePicker({
  id,
  value,
  onChange,
  placeholder = 'Pick a date',
  disabled,
  className,
  fromYear = 1920,
  toYear = new Date().getFullYear(),
}: DatePickerProps) {
  const [open, setOpen] = React.useState(false);
  const [month, setMonth] = React.useState<Date | undefined>(value);
  const [inputValue, setInputValue] = React.useState(formatDate(value));

  // Sync input value when external value changes
  React.useEffect(() => {
    setInputValue(formatDate(value));
    if (value) {
      setMonth(value);
    }
  }, [value]);

  return (
    <div className={cn('relative flex gap-2', className)}>
      <Input
        id={id}
        value={inputValue}
        placeholder={placeholder}
        disabled={disabled}
        className="bg-background pr-10"
        onChange={(e) => {
          const date = new Date(e.target.value);
          setInputValue(e.target.value);
          if (isValidDate(date)) {
            onChange?.(date);
            setMonth(date);
          }
        }}
        onKeyDown={(e) => {
          if (e.key === 'ArrowDown' && !disabled) {
            e.preventDefault();
            setOpen(true);
          }
        }}
      />
      <Popover open={open} onOpenChange={setOpen}>
        <PopoverTrigger asChild>
          <Button
            type="button"
            variant="ghost"
            disabled={disabled}
            className="absolute right-2 top-1/2 size-6 -translate-y-1/2"
          >
            <CalendarIcon className="size-3.5" />
            <span className="sr-only">Select date</span>
          </Button>
        </PopoverTrigger>
        <PopoverContent
          className="w-auto overflow-hidden p-0"
          align="end"
          alignOffset={-8}
          sideOffset={10}
        >
          <Calendar
            mode="single"
            selected={value}
            captionLayout="dropdown"
            month={month}
            fromYear={fromYear}
            toYear={toYear}
            onMonthChange={setMonth}
            onSelect={(date) => {
              onChange?.(date);
              setInputValue(formatDate(date));
              setOpen(false);
            }}
            initialFocus
          />
        </PopoverContent>
      </Popover>
    </div>
  );
}
