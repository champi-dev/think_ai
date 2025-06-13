#!/usr/bin/env node

import { Command } from 'commander';
import chalk from 'chalk';
import ora from 'ora';
import inquirer from 'inquirer';
import { ThinkAI } from './core';
import * as fs from 'fs/promises';
import * as path from 'path';

const program = new Command();
const ai = new ThinkAI();

program
  .name('think')
  .description('AI-powered coding assistant with vector search')
  .version('0.1.0');

// Search command
program
  .command('search <query>')
  .description('Search for similar code patterns')
  .option('-n, --number <number>', 'number of results', '5')
  .option('-l, --language <language>', 'filter by language')
  .action(async (query, options) => {
    const spinner = ora('Searching...').start();
    
    try {
      await ai.initialize();
      const results = await ai.search(query, parseInt(options.number));
      spinner.succeed('Search complete');
      
      if (results.length === 0) {
        console.log(chalk.yellow('No results found. Try adding some code first with "think add"'));
        return;
      }
      
      console.log(chalk.bold(`\nFound ${results.length} similar code patterns:\n`));
      
      results.forEach((result, i) => {
        if (options.language && result.metadata.language !== options.language) {
          return;
        }
        
        console.log(chalk.blue(`${i + 1}. ${result.metadata.description}`));
        console.log(chalk.dim(`   Language: ${result.metadata.language} | Similarity: ${(result.score * 100).toFixed(1)}%`));
        console.log(chalk.gray('   ' + result.code.substring(0, 100) + '...'));
        console.log();
      });
    } catch (error) {
      spinner.fail('Search failed');
      console.error(chalk.red(error.message));
    }
  });

// Add command
program
  .command('add')
  .description('Add code to the knowledge base')
  .option('-f, --file <file>', 'code file to add')
  .option('-c, --code <code>', 'code snippet')
  .option('-l, --language <language>', 'programming language')
  .option('-d, --description <description>', 'description')
  .option('-t, --tags <tags...>', 'tags')
  .action(async (options) => {
    let code: string;
    
    if (options.file) {
      code = await fs.readFile(options.file, 'utf-8');
    } else if (options.code) {
      code = options.code;
    } else {
      console.error(chalk.red('Error: Provide either --file or --code'));
      return;
    }
    
    const spinner = ora('Adding to knowledge base...').start();
    
    try {
      await ai.initialize();
      const index = await ai.addCode(
        code,
        options.language || 'unknown',
        options.description || 'No description',
        options.tags || []
      );
      
      spinner.succeed(`Added successfully! (Index: ${index})`);
    } catch (error) {
      spinner.fail('Failed to add code');
      console.error(chalk.red(error.message));
    }
  });

// Generate command
program
  .command('generate <prompt>')
  .description('Generate code based on prompt')
  .option('-l, --language <language>', 'target language', 'javascript')
  .option('-o, --output <file>', 'save to file')
  .action(async (prompt, options) => {
    const spinner = ora('Generating code...').start();
    
    try {
      await ai.initialize();
      const code = await ai.generateCode(prompt, options.language);
      spinner.succeed('Code generated');
      
      console.log(chalk.green('\nGenerated code:'));
      console.log(code);
      
      if (options.output) {
        await fs.writeFile(options.output, code);
        console.log(chalk.green(`\n✓ Saved to ${options.output}`));
      }
    } catch (error) {
      spinner.fail('Generation failed');
      console.error(chalk.red(error.message));
    }
  });

// Stats command
program
  .command('stats')
  .description('Show knowledge base statistics')
  .action(async () => {
    const spinner = ora('Loading stats...').start();
    
    try {
      await ai.initialize();
      const stats = await ai.getStats();
      spinner.succeed('Stats loaded');
      
      console.log(chalk.bold('\nThink AI Knowledge Base Statistics'));
      console.log(chalk.cyan('Total Snippets:'), stats.totalSnippets);
      console.log(chalk.cyan('Total Characters:'), stats.totalCharacters.toLocaleString());
      
      if (stats.languages && Object.keys(stats.languages).length > 0) {
        console.log(chalk.bold('\nLanguages:'));
        Object.entries(stats.languages).forEach(([lang, count]) => {
          console.log(`  • ${lang}: ${count} snippets`);
        });
      }
    } catch (error) {
      spinner.fail('Failed to load stats');
      console.error(chalk.red(error.message));
    }
  });

// Interactive mode
program
  .command('interactive')
  .description('Start interactive mode')
  .action(async () => {
    console.log(chalk.bold.cyan('Think AI Interactive Mode'));
    console.log(chalk.dim('Commands: search, generate, stats, exit\n'));
    
    await ai.initialize();
    
    while (true) {
      const { command } = await inquirer.prompt([
        {
          type: 'input',
          name: 'command',
          message: 'think>',
        }
      ]);
      
      if (command.toLowerCase() === 'exit') {
        console.log(chalk.yellow('Goodbye!'));
        break;
      }
      
      if (command.startsWith('search ')) {
        const query = command.substring(7);
        const results = await ai.search(query, 3);
        
        results.forEach((result, i) => {
          console.log(chalk.blue(`${i + 1}. ${result.metadata.description} (${(result.score * 100).toFixed(1)}%)`));
        });
      } else if (command.startsWith('generate ')) {
        const prompt = command.substring(9);
        const code = await ai.generateCode(prompt);
        console.log(chalk.green(code));
      } else if (command === 'stats') {
        const stats = await ai.getStats();
        console.log(`Snippets: ${stats.totalSnippets}`);
      } else {
        console.log(chalk.red('Unknown command'));
      }
      
      console.log();
    }
  });

program.parse();