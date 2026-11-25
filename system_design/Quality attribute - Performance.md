##### Quality attribute -> Performance



###### *Response time(End to end latency) = Processing time + waiting time*



**Processing time**: Time spent in our system **actively process** in the request and building/sending the response.



**Waiting time(Latency)**: Duration of the time request/response spends **inactively** in our system.



###### Performance definitions -> **Throughput**

1. **Amount of work performed by our system per unit of time**

   * Measured in tasks/second
2. **Amount of data processed by our system per unit of time**

   * Measured in bits/second, Bytes/second, Mbytes/second



###### Important considerations:

1. Measuring response time correctly
2. Response time distribution

   * What is the **metric** that we should:

     * Set our goal around
     * Measure
   * Average?
   * Median?
   * Maximum?



###### *"Bucket the response time in the histogram"*



Percentile: The **"xth percentile"** is the value below which **x%** of the values can be found



Tail latency: The **small percentage** of the **response times** from a system, that take the **longest** in **comparison** to the **rest** of values



##### *"Shorter Tail => Better"*



3\. Performance degradation

     * Potential overly-utilized resources:

       1. High **CPU** utilization
       2. High **memory** consumption
       3. Too many **connections / IO**
       4. Message **queue** is at capacity









