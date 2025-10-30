import { Link } from 'react-router-dom';
import { Brain, Sparkles, Zap, Shield, ArrowRight, CheckCircle2 } from 'lucide-react';
import Button from '../components/Common/Button';

export default function Landing() {
  const features = [
    {
      icon: Sparkles,
      title: 'Open-Source AI',
      description: 'Powered by Qwen3 and other cutting-edge open-source models',
    },
    {
      icon: Zap,
      title: 'Lightning Fast',
      description: 'Real-time streaming responses with optimized performance',
    },
    {
      icon: Shield,
      title: 'Privacy First',
      description: 'Runs on Think AI\'s private server - your data stays secure',
    },
  ];

  const benefits = [
    'Multi-user support with separate conversations',
    'Beautiful, modern UI with 3D background',
    'Code highlighting and markdown support',
    'Conversation history and management',
    'Multiple open-source AI models (Qwen3 & more)',
    'Free to use - no API costs or subscriptions',
  ];

  return (
    <div className="w-full h-full overflow-y-auto overflow-x-hidden">
      {/* Hero Section */}
      <div className="min-h-full py-8 sm:py-12 lg:py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl 2xl:max-w-[1920px] mx-auto w-full">
          <div className="text-center">
            {/* Logo */}
            <div className="flex justify-center mb-6 sm:mb-8 lg:mb-10">
              <div className="w-16 h-16 sm:w-20 sm:h-20 lg:w-24 lg:h-24 2xl:w-32 2xl:h-32 bg-gradient-to-br from-primary via-accent-1 to-accent-2 rounded-3xl flex items-center justify-center transform hover:rotate-12 transition-transform duration-300">
                <Brain className="w-8 h-8 sm:w-10 sm:h-10 lg:w-12 lg:h-12 2xl:w-16 2xl:h-16 text-white" />
              </div>
            </div>

            {/* Title */}
            <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl 2xl:text-8xl font-bold mb-4 sm:mb-6 lg:mb-8 bg-gradient-to-r from-primary via-accent-1 to-accent-2 text-transparent bg-clip-text px-2">
              Think AI
            </h1>
            <p className="text-lg sm:text-xl md:text-2xl lg:text-3xl 2xl:text-4xl text-text-secondary mb-3 sm:mb-4 lg:mb-6 px-4">
              Your Personal AI Assistant
            </p>
            <p className="text-sm sm:text-base md:text-lg lg:text-xl 2xl:text-2xl text-text-tertiary max-w-xl sm:max-w-2xl lg:max-w-3xl 2xl:max-w-5xl mx-auto mb-8 sm:mb-10 lg:mb-12 px-4 leading-relaxed">
              Harness the power of open-source AI models running privately on Think AI's server. Currently powered by Qwen3 with more models coming soon. Fast, private, and free to use.
            </p>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row gap-3 sm:gap-4 lg:gap-6 justify-center items-stretch sm:items-center mb-10 sm:mb-12 lg:mb-16 px-4 max-w-2xl mx-auto">
              <Link to="/register" className="w-full sm:w-auto">
                <Button variant="primary" className="w-full sm:w-auto px-6 sm:px-8 lg:px-10 2xl:px-12 py-2.5 sm:py-3 lg:py-4 text-base sm:text-lg lg:text-xl 2xl:text-2xl group">
                  Get Started Free
                  <ArrowRight className="ml-2 w-4 h-4 sm:w-5 sm:h-5 lg:w-6 lg:h-6 group-hover:translate-x-1 transition-transform" />
                </Button>
              </Link>
              <Link to="/login" className="w-full sm:w-auto">
                <Button variant="secondary" className="w-full sm:w-auto px-6 sm:px-8 lg:px-10 2xl:px-12 py-2.5 sm:py-3 lg:py-4 text-base sm:text-lg lg:text-xl 2xl:text-2xl">
                  Sign In
                </Button>
              </Link>
            </div>

            {/* Features Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6 lg:gap-8 2xl:gap-10 mb-10 sm:mb-12 lg:mb-16 px-2">
              {features.map((feature, index) => (
                <div
                  key={index}
                  className="bg-bg-secondary/50 backdrop-blur-xl border border-border-primary rounded-xl sm:rounded-2xl p-4 sm:p-6 lg:p-8 2xl:p-10 hover:border-primary/50 transition-all hover:transform hover:-translate-y-2 duration-300"
                >
                  <div className="w-10 h-10 sm:w-12 sm:h-12 lg:w-14 lg:h-14 2xl:w-16 2xl:h-16 bg-primary/10 rounded-lg sm:rounded-xl flex items-center justify-center mb-3 sm:mb-4 lg:mb-5 mx-auto">
                    <feature.icon className="w-5 h-5 sm:w-6 sm:h-6 lg:w-7 lg:h-7 2xl:w-8 2xl:h-8 text-primary" />
                  </div>
                  <h3 className="text-lg sm:text-xl lg:text-2xl 2xl:text-3xl font-semibold mb-2 sm:mb-3">{feature.title}</h3>
                  <p className="text-sm sm:text-base lg:text-lg 2xl:text-xl text-text-secondary leading-relaxed">{feature.description}</p>
                </div>
              ))}
            </div>

            {/* Benefits Section */}
            <div className="bg-bg-secondary/30 backdrop-blur-xl border border-border-primary rounded-xl sm:rounded-2xl p-5 sm:p-8 lg:p-10 2xl:p-12 max-w-xs sm:max-w-3xl lg:max-w-4xl 2xl:max-w-6xl mx-auto mb-10 sm:mb-12 lg:mb-16">
              <h2 className="text-2xl sm:text-3xl lg:text-4xl 2xl:text-5xl font-bold mb-4 sm:mb-6 lg:mb-8">What You Get</h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4 lg:gap-5 2xl:gap-6 text-left">
                {benefits.map((benefit, index) => (
                  <div key={index} className="flex items-start gap-2 sm:gap-3 lg:gap-4">
                    <CheckCircle2 className="w-4 h-4 sm:w-5 sm:h-5 lg:w-6 lg:h-6 2xl:w-7 2xl:h-7 text-primary flex-shrink-0 mt-0.5 sm:mt-1" />
                    <span className="text-sm sm:text-base lg:text-lg 2xl:text-xl text-text-secondary leading-relaxed">{benefit}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="border-t border-border-primary bg-bg-secondary/30 backdrop-blur-xl py-4 sm:py-6 lg:py-8 2xl:py-10 px-4 sm:px-6 lg:px-8 mt-auto">
        <div className="max-w-7xl 2xl:max-w-[1920px] mx-auto text-center">
          <p className="text-text-tertiary text-xs sm:text-sm lg:text-base 2xl:text-lg">
            Powered by Qwen3 and other open-source AI models via Ollama
          </p>
          <p className="text-text-tertiary text-xs sm:text-xs lg:text-sm 2xl:text-base mt-1 sm:mt-2 lg:mt-3">
            Built with React, Express, and PostgreSQL • 100% Open Source
          </p>
        </div>
      </footer>
    </div>
  );
}
