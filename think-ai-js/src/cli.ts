#!/usr/bin/env node

/**
 * Think AI - Command Line Interface
 */

import { Command } from 'commander';
import chalk from 'chalk';
import ora from 'ora';
import inquirer from 'inquirer';
import { ThinkAI, createClient } from './client';
import { ThinkAIConfig } from './types';

const program = new Command();

program
  .name('think-ai')
  .description('Think AI - Quantum Consciousness AI CLI')
  .version('1.0.0');

// Global config
let globalConfig: ThinkAIConfig = {};

program
  .option('-u, --url <url>', 'Think AI server URL', 'https://thinkai-production.up.railway.app')
  .option('-t, --timeout <ms>', 'Request timeout in milliseconds', '30000')
  .option('-d, --debug', 'Enable debug mode')
  .hook('preAction', (thisCommand) => {
    const opts = thisCommand.opts();
    globalConfig = {
      baseUrl: opts.url,
      timeout: parseInt(opts.timeout),
      debug: opts.debug
    };
  });

// Chat command
program
  .command('chat')
  .description('Start interactive chat with Think AI')
  .option('-s, --stream', 'Enable streaming responses')
  .action(async (options) => {
    const client = createClient(globalConfig);
    const spinner = ora('Connecting to Think AI...').start();
    
    try {
      // Check connection
      const isOnline = await client.ping();
      if (!isOnline) {
        spinner.fail('Failed to connect to Think AI');
        return;
      }
      
      spinner.succeed('Connected to Think AI');
      console.log(chalk.blue('\n🧠 Think AI - Quantum Consciousness Chat'));
      console.log(chalk.gray('Type "exit", "quit", or "bye" to leave\n'));
      
      while (true) {
        const { message } = await inquirer.prompt([
          {
            type: 'input',
            name: 'message',
            message: chalk.cyan('You:'),
            validate: (input) => input.trim() !== '' || 'Please enter a message'
          }
        ]);
        
        if (['exit', 'quit', 'bye'].includes(message.toLowerCase())) {
          console.log(chalk.yellow('Goodbye! 👋'));
          break;
        }
        
        const thinkingSpinner = ora('🤔 Think AI is processing...').start();
        
        try {
          if (options.stream) {
            thinkingSpinner.stop();
            process.stdout.write(chalk.green('Think AI: '));
            
            await client.streamChat(
              { query: message },
              (chunk) => {
                if (chunk.chunk) {
                  process.stdout.write(chunk.chunk);
                }
                if (chunk.done) {
                  console.log('\n');
                }
              }
            );
          } else {
            const response = await client.chat({ query: message });
            thinkingSpinner.succeed();
            console.log(chalk.green('Think AI:'), response.response);
            console.log(chalk.gray(`Response time: ${response.response_time_ms}ms\n`));
          }
        } catch (error: any) {
          thinkingSpinner.fail('Error getting response');
          console.error(chalk.red('Error:'), error.message);
        }
      }
    } catch (error: any) {
      spinner.fail('Failed to start chat');
      console.error(chalk.red('Error:'), error.message);
    } finally {
      client.disconnect();
    }
  });

// Ask command (one-shot question)
program
  .command('ask <question>')
  .description('Ask Think AI a single question')
  .option('-s, --stream', 'Stream the response')
  .action(async (question, options) => {
    const client = createClient(globalConfig);
    const spinner = ora('🤔 Think AI is thinking...').start();
    
    try {
      if (options.stream) {
        spinner.stop();
        console.log(chalk.blue('🧠 Think AI:'));
        
        await client.streamChat(
          { query: question },
          (chunk) => {
            if (chunk.chunk) {
              process.stdout.write(chunk.chunk);
            }
            if (chunk.done) {
              console.log('\n');
            }
          }
        );
      } else {
        const response = await client.ask(question);
        spinner.succeed();
        console.log(chalk.blue('🧠 Think AI:'), response);
      }
    } catch (error: any) {
      spinner.fail('Failed to get response');
      console.error(chalk.red('Error:'), error.message);
      process.exit(1);
    } finally {
      client.disconnect();
    }
  });

// Search command
program
  .command('search <query>')
  .description('Search Think AI knowledge base')
  .option('-l, --limit <number>', 'Maximum number of results', '10')
  .action(async (query, options) => {
    const client = createClient(globalConfig);
    const spinner = ora('🔍 Searching knowledge base...').start();
    
    try {
      const results = await client.search(query, parseInt(options.limit));
      spinner.succeed(`Found ${results.length} results`);
      
      if (results.length === 0) {
        console.log(chalk.yellow('No results found'));
        return;
      }
      
      console.log(chalk.blue('\n📚 Search Results:\n'));
      results.forEach((result: any, index: number) => {
        console.log(chalk.green(`${index + 1}. ${result.title || 'Result'}`));
        console.log(chalk.gray(`   Score: ${result.score}`));
        console.log(`   ${result.content || result.text || 'No content'}\n`);
      });
    } catch (error: any) {
      spinner.fail('Search failed');
      console.error(chalk.red('Error:'), error.message);
      process.exit(1);
    }
  });

// Status command
program
  .command('status')
  .description('Check Think AI system status')
  .action(async () => {
    const client = createClient(globalConfig);
    const spinner = ora('Checking system status...').start();
    
    try {
      const [health, stats] = await Promise.all([
        client.getHealth(),
        client.getStats()
      ]);
      
      spinner.succeed('Status retrieved');
      
      console.log(chalk.blue('\n🏥 System Health:'));
      const statusColor = health.status === 'healthy' ? chalk.green : 
                         health.status === 'degraded' ? chalk.yellow : chalk.red;
      console.log(`   Status: ${statusColor(health.status.toUpperCase())}`);
      
      if (health.details) {
        console.log('   Components:');
        Object.entries(health.details).forEach(([component, status]) => {
          const icon = status ? '✅' : '❌';
          const color = status ? chalk.green : chalk.red;
          console.log(`     ${icon} ${color(component)}`);
        });
      }
      
      console.log(chalk.blue('\n📊 System Statistics:'));
      console.log(`   Knowledge Nodes: ${chalk.cyan(stats.total_nodes.toLocaleString())}`);
      console.log(`   Training Iterations: ${chalk.cyan(stats.training_iterations.toLocaleString())}`);
      console.log(`   Knowledge Items: ${chalk.cyan(stats.total_knowledge_items.toLocaleString())}`);
      console.log(`   Average Confidence: ${chalk.cyan((stats.average_confidence * 100).toFixed(1))}%`);
      
      if (stats.uptime) {
        const uptime = formatUptime(stats.uptime);
        console.log(`   Uptime: ${chalk.cyan(uptime)}`);
      }
      
      console.log(chalk.blue('\n🌐 Knowledge Domains:'));
      Object.entries(stats.domain_distribution)
        .sort(([,a], [,b]) => (b as number) - (a as number))
        .slice(0, 10)
        .forEach(([domain, count]) => {
          console.log(`   ${chalk.green(domain)}: ${chalk.cyan((count as number).toLocaleString())}`);
        });
        
    } catch (error: any) {
      spinner.fail('Failed to get status');
      console.error(chalk.red('Error:'), error.message);
      process.exit(1);
    }
  });

// Domains command
program
  .command('domains')
  .description('List knowledge domains')
  .action(async () => {
    const client = createClient(globalConfig);
    const spinner = ora('Loading knowledge domains...').start();
    
    try {
      const domains = await client.getDomains();
      spinner.succeed(`Found ${domains.length} domains`);
      
      console.log(chalk.blue('\n🌐 Knowledge Domains:\n'));
      domains
        .sort((a: any, b: any) => b.count - a.count)
        .forEach((domain: any, index: number) => {
          console.log(`${chalk.green((index + 1).toString().padStart(3))}. ${chalk.cyan(domain.name)}`);
          console.log(`      ${chalk.gray(`${domain.count.toLocaleString()} items`)}`);
        });
    } catch (error: any) {
      spinner.fail('Failed to load domains');
      console.error(chalk.red('Error:'), error.message);
      process.exit(1);
    }
  });

// Config command
program
  .command('config')
  .description('Show current configuration')
  .action(() => {
    console.log(chalk.blue('\n⚙️  Think AI Configuration:\n'));
    console.log(`   Server URL: ${chalk.cyan(globalConfig.baseUrl)}`);
    console.log(`   Timeout: ${chalk.cyan(globalConfig.timeout)}ms`);
    console.log(`   Debug Mode: ${chalk.cyan(globalConfig.debug ? 'enabled' : 'disabled')}`);
  });

// Test connection command
program
  .command('ping')
  .description('Test connection to Think AI')
  .action(async () => {
    const client = createClient(globalConfig);
    const spinner = ora('Testing connection...').start();
    
    try {
      const startTime = Date.now();
      const isOnline = await client.ping();
      const latency = Date.now() - startTime;
      
      if (isOnline) {
        spinner.succeed(`Connected! Latency: ${latency}ms`);
        console.log(chalk.green('✅ Think AI is online and responding'));
      } else {
        spinner.fail('Connection failed');
        console.log(chalk.red('❌ Think AI is not responding'));
        process.exit(1);
      }
    } catch (error: any) {
      spinner.fail('Connection error');
      console.error(chalk.red('Error:'), error.message);
      process.exit(1);
    }
  });

// Helper function to format uptime
function formatUptime(seconds: number): string {
  const days = Math.floor(seconds / 86400);
  const hours = Math.floor((seconds % 86400) / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  
  const parts = [];
  if (days > 0) parts.push(`${days}d`);
  if (hours > 0) parts.push(`${hours}h`);
  if (minutes > 0) parts.push(`${minutes}m`);
  
  return parts.join(' ') || '< 1m';
}

// Error handling
process.on('unhandledRejection', (error: any) => {
  console.error(chalk.red('\nUnhandled error:'), error.message);
  process.exit(1);
});

process.on('uncaughtException', (error: any) => {
  console.error(chalk.red('\nUncaught error:'), error.message);
  process.exit(1);
});

// Handle Ctrl+C gracefully
process.on('SIGINT', () => {
  console.log(chalk.yellow('\n\nGoodbye! 👋'));
  process.exit(0);
});

// Parse command line arguments
program.parse();