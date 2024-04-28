// using System;
// using System.Collections.Generic;
using System.Text.Json;
using System.Text.Json.Serialization;

namespace ApproxScore
{
    class Program
    {
        static void Main(string[] args)
        {
            if (args.Length < 2)
            {
                Console.WriteLine("Usage: TextSearchProgram <searchable_list> <to_search>");
                return;
            }

            // Console.WriteLine("args[0]:" + args[0] + "___");
            string[] searchableList = JsonSerializer.Deserialize<string[]>(args[0]);
            // Console.WriteLine("searchableList:" + searchableList + "___");
            string toSearch = args[1];

            List<(string, int)> scores = new List<(string, int)>();

            foreach (string item in searchableList)
            {
                // Console.WriteLine("item" + item);
                int score = HowStringsMatch(item, toSearch);
                scores.Add((item, score));
            }

            // Serialize the list of tuples using a custom converter
            JsonSerializerOptions options = new JsonSerializerOptions
            {
                Converters = { new TupleConverter() },
                WriteIndented = true // Optional: makes the JSON output formatted for readability
            };
            string jsonOutput = JsonSerializer.Serialize(scores, options);

            // string jsonOutput = JsonSerializer.Serialize<List<(string, int)>>(scores);
            Console.WriteLine(jsonOutput);
            // foreach (var item in scores)
            // {
            //     Console.WriteLine(item);
            // }
        }

        // Custom converter for tuples
        public class TupleConverter : JsonConverter<(string, int)>
        {
            public override (string, int) Read(ref Utf8JsonReader reader, Type typeToConvert, JsonSerializerOptions options)
            {
                throw new NotImplementedException();
            }

            public override void Write(Utf8JsonWriter writer, (string, int) value, JsonSerializerOptions options)
            {
                writer.WriteStartObject();
                writer.WriteString("item", value.Item1);
                writer.WriteNumber("score", value.Item2);
                writer.WriteEndObject();
            }
        }

        //Compares 2 short strings (to avoid overflow on the returning value) and gives an int representing how much they match
        // String match when: -they share same letters
        //                    -sames letters shared tend to follows themselve (this second part impact more than the first)
        static int HowStringsMatch(string theStrRef, string theStrSearch, bool lExactSearch=false)
        {
            theStrRef = theStrRef.Replace("\r", "").Replace("\n", " ");
            theStrSearch = theStrSearch.Replace("\r", "").Replace("\n", " ");

            int theStrRefLen = theStrRef.Length;
            int theStrSearchLen = theStrSearch.Length;
            int theStrSearchLenMinus1 = theStrSearchLen - 1;

            //if the search string is empty, stop
            if (theStrSearchLen <= 0 || theStrRefLen <= 0)
            {
                return 0;
            }

            //Coefficient that grows with the sequence
            int gain = 1;

            //Create the list of arrays that would contains letter correlation
            List<int[]> list = new List<int[]>(theStrSearchLen);
            for (int i = 0; i < theStrSearchLen; i++)
            {
                list.Add(new int[theStrRefLen]);
            }
            //Create the gainTab (to sum in the end)
            int gainTabSize = 0;
            if (theStrSearchLen > 1)
            {
                gainTabSize = theStrRefLen * (theStrSearchLenMinus1);
            }
            else
            {
                gainTabSize = theStrRefLen;
            }
            int[] gainTab = new int[gainTabSize];
            // theStrSearch.Count();
            //Fill the arrays of the list and put a number at every index that letters of strings match
            for (int i = 0; i < theStrSearchLen; i++)
            {
                for (int j = 0; j < theStrRefLen; j++)
                {
                    if (theStrSearch[i] == theStrRef[j] && theStrSearch[i] != ' ')
                    {
                        list[i][j] = (i + 1);
                    }
                    else
                    {
                        list[i][j] = 0;
                    }
                }
            }
            //Read the arrays of the list and fill an array with a number that grows when number of succession of array are successing
            if (theStrSearchLen > 1)
            {
                int iPlusJ;
                int iPlusJModtheStrRefLen;
                for (int i = 0; i < theStrRefLen; i++)
                {
                    for (int j = 0; j < theStrSearchLenMinus1; j++)
                    {
                        iPlusJ = i + j;
                        iPlusJModtheStrRefLen = (iPlusJ) % theStrRefLen;
                        /* Actual letter is matching a letter in the other array */
                        if (list[j][iPlusJModtheStrRefLen] != 0 && list[j][iPlusJModtheStrRefLen] == list[j + 1][(iPlusJ + 1) % theStrRefLen] - 1)
                        {
                            gainTab[i * (theStrSearchLenMinus1) + j] = gain;
                            //Limitation of the gain to avoid overflow
                            if (gain <= 4)
                            {
                                gain *= 2;
                            }
                        }
                        else
                        {
                            gainTab[i * (theStrSearchLenMinus1) + j] = 0;
                            gain = 1;
                        }
                    }
                }
            }
            else
            {
                // int list0Len = list[0].Count();
                for (int i = 0; i < theStrSearchLenMinus1 - 1; i++)
                {
                    if (list[0][i] == list[0][i + 1] - 1)
                    {
                        gainTab[i] = gain;
                        gain *= 2;
                    }
                    else
                    {
                        gainTab[i] = 0;
                        gain = 1;
                    }
                }
            }

            // try
            // {
            int result = gainTab.Sum();
            if (theStrRef.Contains(theStrSearch))
            {
                if (result > 147483647)
                {
                    result = 2147483647;
                }
                else
                {
                    result += 2000000000;
                }
            }
            else if (lExactSearch)
            {
                result = 0;
            }
            return result;
            // }
            // catch (ArgumentNullException err)
            // {
            //     Console.WriteLine(err + "\n" + list + "\n" + gainTab + "\n" + theStrRef + "\n" + theStrSearch);
            //     return 0;
            // }
        }
    }
}