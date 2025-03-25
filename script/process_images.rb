#!/usr/bin/env ruby
require 'fileutils'

def compress_images_to_webp(src_dir, dest_dir)
  FileUtils.mkdir_p(dest_dir)
  
  Dir.glob("#{src_dir}/*.{jpg,png,jpeg,gif}") do |img|
    next unless File.file?(img)
    
    filename = File.basename(img, ".*")
    output_file = "#{dest_dir}/#{filename}.webp"
    
    system("convert \"#{img}\" -quality 80 -resize 1200x1200\\> \"#{output_file}\"")
    puts "已轉換 #{img} 為 #{output_file}"
  end
end

# Process images before Jekyll build
compress_images_to_webp("assets/images/mao", "compressed_images/mao")

