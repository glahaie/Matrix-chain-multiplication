#! /usr/bin/ruby
# matrices.rb
# exemple de parenthesage pour rb
#

require 'matrix'

def multiplierMatrices(a, b)
    c = Array.new(a.
    0.upto(c.row_count-1) do |i|
        0.upto(c.column_count-1) do |j|
            0.upto(a.column_count-1) do |k|
                c[i, j] += a[i, k] * b[k, j]
            end
        end
    end
    return c
end

a = Matrix.I(5)
b = Matrix.I(5)
c = multiplierMatrices(a,b)
print c
