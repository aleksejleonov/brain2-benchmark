#!/usr/bin/env ruby

BenchmarkResult = Struct.new(
  :building_time,
  :simulation_time,
  :time_step,
  keyword_init: true
)

Benchmark = Struct.new(
  :file_name,
  :benchmark_name,
  :results,
  keyword_init: true
)

class BenchmarkParser
  RESULTS_REGEXP = %r{
    Building\stime.*:\s(?<building_time>[\d.]+.*)\s
    Simulation\stime.*:\s(?<simulation_time>[\d.]+.*)\s
    Time\sstep.*:\s(?<time_step>[\d.]+.*)
  }x
  NAME_REGEXPR = /^Testing.*$/

  def self.for(text:, file_name:)
    results = text.scan(RESULTS_REGEXP).map do |result|
      BenchmarkResult.new(
        building_time: result[0],
        simulation_time: result[1],
        time_step: result[2]
      )
    end

    Benchmark.new(
      file_name: file_name,
      benchmark_name: text.match(NAME_REGEXPR)[0],
      results: results
    )
  end
end

class BenchmarkSplitter
  SPLITTER_REGEXP = /\*{3,}(.*?)\*{3,}/m

  def self.for(text:)
    text.scan(SPLITTER_REGEXP).map(&:first)
  end
end

class BenchmarksFileParser
  attr_reader :file_path

  def self.for(file_path:)
    new(file_path: file_path).benchmarks
  end

  def initialize(file_path:)
    @file_path = file_path
  end

  def benchmarks
    BenchmarkSplitter.for(text: text_cleared).map do |text|
      BenchmarkParser.for(text: text, file_name: name)
    end
  end

  private

  def name
    File.basename(file_path, ".*")
  end

  def text_raw
    File.read(file_path)
  end

  def remove_cpuinfo(text)
    text.split("Benchmark").last
  end

  def remove_warnings(text)
    text.gsub(/^WARNING .*$/, "")
  end

  def normalize_lines(text)
    text.delete("\r").gsub("\n\n\n", "\n\n")
  end

  def text_cleared
    normalize_lines(remove_warnings(remove_cpuinfo(text_raw)))
  end
end

class BenchmarksFilesParser
  def self.for(file_pathes:)
    file_pathes.flat_map do |file_path|
      BenchmarksFileParser.for(file_path: file_path)
    end
  end
end

class MarkdownTableGenerator
  def self.for(benchmarks:)
    benchmarks.group_by(&:benchmark_name).to_a.sort.map do |benchmark_name, benchmarks_group|
      benchmark_columns = benchmarks_group.sort_by(&:file_name)

      benchmark_name_row = "# #{benchmark_name}"
      header_columns = ["Task", *benchmark_columns.map(&:file_name)]
      header_row = header_columns.join(" | ")
      header_divider = [":-", *benchmark_columns.map { "-:" }].join(" | ")

      result_rows = benchmark_columns.map(&:results).transpose.map do |results|
        [
          [
            "Building time",
            "Simulation time"
            # "Time step",
          ].join("<br>"),
          *results.map do |result|
            [
              "`#{result.building_time}`",
              "`#{result.simulation_time}`"
              # "`#{result.time_step}`",
            ].join("<br>")
          end
        ].join(" | ")
      end

      [
        benchmark_name_row,
        header_row,
        header_divider,
        *result_rows,
        "\n\n"
      ].join("\n")
    end
  end
end

puts MarkdownTableGenerator.for(
  benchmarks: BenchmarksFilesParser.for(
    file_pathes: ARGV
  )
)
