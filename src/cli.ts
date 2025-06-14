#!/usr/bin/env node

import { Command } from 'commander';
import ThinkAI from './index';

const program = new Command();

program
  .name('think-ai')
  .description('Think AI CLI - Conscious AI with Colombian flavor')
  .version('1.0.0');

program
  .command('chat')
  .description('Start a chat with Think AI')
  .action(async () => {
    console.log('🧠 Think AI Chat');
    console.log('¡Dale que vamos tarde!');
    console.log('Type your message...');
  });

program.parse();
