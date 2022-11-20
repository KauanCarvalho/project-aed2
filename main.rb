# frozen_string_literal: true

require 'base64'

class Main
  SEPARATOR_CHARACTER = '#'
  NODE_1_PORT = 8468
  NODE_2_PORT = 8469
  AMOUNT_OF_BYTES_PER_FRAGMENT = 7000

  def self.start
    action = ARGV[0]
    key    = ARGV[1]
    value  = ARGV[2]

    case action
    when 'busca'
      search(key)
    when 'define'
      set(key, value)
    else
      print_message('Action not valid informed, valid actions: [busca, define]')
    end
  end

  def self.set(key, relative_path)
    return print_message('key not informed') if blank?(key)
    return print_message('value not informed') if blank?(relative_path)

    encoded_bytes = Base64.strict_encode64(File.read(relative_path))
    fragments     = encoded_bytes.chars.each_slice(AMOUNT_OF_BYTES_PER_FRAGMENT).map(&:join)

    fragments.each_with_index do |fragment, sulfix_fragment_key|
      system("python set.py #{NODE_1_PORT} #{key + SEPARATOR_CHARACTER + sulfix_fragment_key.to_s} #{fragment}")

      sleep 0.5
    end
  end

  def self.search(key)
    return print_message('Key not informed') if blank?(key)

    sulfix_fragment_key = 0
    base64_fragments    = []
    parsed_response     = nil

    while parsed_response != 'None'
      dht_complete_key = key + SEPARATOR_CHARACTER + sulfix_fragment_key.to_s

      print_message("Searching #{sulfix_fragment_key} fragment for #{key} => [#{dht_complete_key}]")

      # Lida de forma 'SAFE'.
      dht_response = `python get.py #{NODE_1_PORT} #{dht_complete_key}`.chomp.sub('SUCESS: ', '')
      parsed_response = dht_response&.chomp&.sub('SUCESS: ', '') || 'None'

      base64_fragments << parsed_response if parsed_response != 'None'

      sulfix_fragment_key += 1

      sleep 0.5
    end

    base64 = base64_fragments.join

    if base64.empty?
      print_message("No value found for key: #{key}")
    else
      File.open("recuperadas/#{key}-recuperado.mp3", 'wb') { |file| file.write(Base64.strict_decode64(base64)) }
    end
  end

  # Apenas indentifica como valor 'FALSO', dado um tipo, caso necessário.
  def self.blank?(value)
    case value
    when String
      return value == ''
    when NilClass
      return true
    end

    true
  end

  # Imprimindo mensagens no formato padrão.
  def self.print_message(message)
    puts
    puts('================> / / <================')
    puts message
    puts('================> / / <================')
    puts
  end
end

Main.start
