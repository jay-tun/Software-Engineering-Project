import requests
from requests.exceptions import HTTPError

"""
The code has been extensively modified referring to the authors previous code. Previously, 
only three aggregation functions were implemented, namely min, max and average and they were
hard-coded as well. Therefore the codebase is improved to include dynamical query structuring
for database interactions rather than hard-coding.
"""


"""
Create multiple classes and split functions into smaller functions for better readibility.
Implemented new class CoverageConstructor to create your own coverages if the user doesn't want
to utilize the existing ones in WCPS.
"""

class DatabaseConnection:
    """
    Manages HTTP connections to a database server to facilitate the sending of queries.
    This class abstracts the details of network communications using HTTP POST requests.
    """
    def __init__(self, server_url):
        """
        Initialize a new DatabaseConnection instance.
        
        Args:
            server_url (str): The URL of the database server where queries will be sent.
        """
        self.server_url = server_url

    def send_request(self, query):
        """
        Sends a POST request to the configured database server with the specified query.
        
        Args:
            query (str): The WCPS or query language string to be executed by the database server.
        
        Returns:
            requests.Response: The response object containing HTTP status, headers, and payload returned by the server.
        
        Raises:
            HTTPError: An error from the requests library for responses with HTTP error status codes.
            Exception: Catches other general exceptions related to network failures or decoding issues.
        """
        try:
            response = requests.post(self.server_url, data={'query': query}, verify=False)
            response.raise_for_status()  # Raises HTTPError for bad responses (4XX or 5XX)
            return response
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")  # Print and handle HTTP-specific errors
            return None
        except Exception as err:
            print(f"An error occurred: {err}")  # Print and handle other exceptions like network errors
            return None


class Coverage:
    """
    Represents a specific dataset or "coverage" in a database, typically used in geospatial data systems.
    This class allows specifying subsets of data through axis parameters and supports operations on the data.
    """
    coverage_counter = 1  # Class variable to make sure each coverage has a unique variable
    def __init__(self, name):
        """
        Initializes a new instance of the Coverage class.

        Args:
            name (str): The name of the dataset or coverage as recognized by the database.
        """
        self.name = name
        self.variable = f'c{Coverage.coverage_counter}'  # Unique identifier for this instance
        Coverage.coverage_counter += 1  # Increment the counter for each new instance
        self.subset = None  # To hold subset specifications if set

    def __str__(self):
        """
        String representation of the Coverage instance, showing its unique variable and any subset defined.

        Returns:
            str: The string representation of the Coverage object.
        """
        if self.subset:
            return f'${self.variable}{self.subset}'
        else:
            return f'${self.variable}'

    def set_subset(self, *args):
        """
        Sets the subset parameters for the coverage using specified axes.

        Args:
            *args: A variable number of Axis objects that define the subset parameters.

        Raises:
            ValueError: If any argument is not an instance of the Axis class.
        """
        for arg in args:
            if not isinstance(arg, Axis):
                raise ValueError("All arguments must be instances of Axis")
        axes_str = ', '.join(str(axis) for axis in args)  # Convert axes to string representation
        self.subset = f'[{axes_str}]'  # Format and store the subset parameters

    # These methods enable arithmetic and comparison operations between Coverage instances or with other values.
    # Each operation returns a new BinaryOperation object representing the operation between two operands.
    def __add__(self, other):
        return BinaryOperation(self, '+', other)

    def __sub__(self, other):
        return BinaryOperation(self, '-', other)

    def __mul__(self, other):
        return BinaryOperation(self, '*', other)

    def __truediv__(self, other):
        return BinaryOperation(self, '/', other)

    def __lt__(self, other):
        return BinaryOperation(self, '<', other)

    def __le__(self, other):
        return BinaryOperation(self, '<=', other)

    def __gt__(self, other):
        return BinaryOperation(self, '>', other)

    def __ge__(self, other):
        return BinaryOperation(self, '>=', other)

    def __eq__(self, other):
        return BinaryOperation(self, '==', other)

    def __ne__(self, other):
        return BinaryOperation(self, '!=', other)


class Axis:
    """
    Represents an axis in a multidimensional data space, commonly used in geospatial and scientific data.
    An axis defines a dimension of the dataset that can be used to specify a subset of the data.
    """

    def __init__(self, name, lower_bound, upper_bound=None):
        """
        Initializes an Axis instance, which defines a range or a single point along a dimension.

        Args:
            name (str): The name of the axis, e.g., 'time', 'latitude', 'longitude'.
            lower_bound (int or str): The lower bound of the axis range. If upper_bound is None, this
                                      represents a single specific value on this axis.
            upper_bound (int or str, optional): The upper bound of the axis range. If None, the axis
                                                is considered to represent a single point.
        """
        self.name = name
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def __str__(self):
        """
        Returns a string representation of the Axis, showing its bounds or single value.

        Returns:
            str: A formatted string representing the range or point of this axis.
        """
        if self.upper_bound is None:
            return f"{self.name}({self.lower_bound})"
        else:
            return f"{self.name}({self.lower_bound}:{self.upper_bound})"
        
class BinaryOperation:
    """
    Represents a binary operation between two operands. This class is used to construct
    and represent expressions in a symbolic form, typically for building query strings
    or for computational purposes within data manipulation frameworks.
    """

    def __init__(self, lhs, operator, rhs):
        """
        Initializes a BinaryOperation instance.

        Args:
            lhs: The left-hand side operand of the binary operation.
            rhs: The right-hand side operand of the binary operation.
            operator (str): The operator symbol as a string, such as '+', '-', '*', '/', '<', '>', etc.
                            Special handling for '==' to conform with certain query languages like WCPS.
        """
        self.lhs = lhs
        self.rhs = rhs
        self.operator = operator

    def __str__(self):
        """
        Returns a string representation of the binary operation, adjusting for query language specifics.

        Returns:
            str: A string that represents the binary operation, using the appropriate operator symbols.
        """
        # Adjust for operators like '==' that needs to be represented differently in WCPS.
        operator = '=' if self.operator == '==' else self.operator
        return f'({self.lhs} {operator} {self.rhs})'

    # Below are the special methods to support arithmetic operations directly with instances of this class.

    def __add__(self, other):
        return BinaryOperation(self, '+', other)

    def __sub__(self, other):
        return BinaryOperation(self, '-', other)

    def __mul__(self, other):
        return BinaryOperation(self, '*', other)

    def __truediv__(self, other):
        return BinaryOperation(self, '/', other)

    def __lt__(self, other):
        return BinaryOperation(self, '<', other)

    def __le__(self, other):
        return BinaryOperation(self, '<=', other)

    def __gt__(self, other):
        return BinaryOperation(self, '>', other)

    def __ge__(self, other):
        return BinaryOperation(self, '>=', other)

    def __eq__(self, other):
        return BinaryOperation(self, '==', other)

    def __ne__(self, other):
        return BinaryOperation(self, '!=', other)


class RGBColor:
    """
    Represents a color using the RGB color model, which combines red, green, and blue light
    in various ways to reproduce a broad array of colors.
    """

    def __init__(self, red, green, blue):
        """
        Initializes an RGBColor instance with specific color values.

        Args:
            red (int): The intensity of the red component, typically between 0 and 255.
            green (int): The intensity of the green component, typically between 0 and 255.
            blue (int): The intensity of the blue component, typically between 0 and 255.
        """
        self.red = red
        self.green = green
        self.blue = blue

    def __str__(self):
        """
        Returns a string representation of the RGB color in a common CSS format.

        Returns:
            str: A string that represents the color in 'red: x; green: y; blue: z;' format.
        """
        return f"{{red: {self.red}; green: {self.green}; blue: {self.blue}}}"


class Case:
    """
    Represents a conditional case in a switch-like statement structure, used for decision making based on 
    the result of an expression, and returning a corresponding RGB color.
    """

    def __init__(self, expression, RGBColor):
        """
        Initializes a Case instance with an expression and an associated RGB color.

        Args:
            expression (str or BinaryOperation): The condition to evaluate, typically involving comparisons or logical operations.
            RGBColor (RGBColor): The RGBColor object to return if the condition evaluates as true.
        """
        self.expression = expression
        self.RGBColor = RGBColor

    def __str__(self):
        """
        Returns a string representation of the case statement formatted for usage in WCPS queries.

        Returns:
            str: A string that represents the case condition and the RGB color to return, formatted for readability.
        """
        return f"case {self.expression}\n\t\treturn {self.RGBColor}"


class Switch:
    """
    Represents a switch-like structure for decision making in WCPS queries.
    """

    def __init__(self, RGBColor):
        """
        Initializes a Switch instance with an RGBColor to be returned for the default case.

        Args:
            RGBColor (RGBColor): The RGBColor object to be returned if no cases match.
        """
        self.cases = []
        self.RGBColor = RGBColor

    def add_case(self, case):
        """
        Adds a Case object to the list of cases in the switch statement.

        Args:
            case (Case): The Case object representing a conditional case.
        Raises:
            TypeError: If the provided case is not an instance of Case.
        """
        if not isinstance(case, Case):
            raise TypeError("case must be an instance of Case")
        self.cases.append(case)

    def __str__(self):
        """
        Returns a string representation of the switch statement formatted for usage in WCPS queries.

        Returns:
            str: A string representing the switch statement and its cases, formatted for readability.
        """
        switch_statement = "switch\n"
        for case in self.cases:
            case_str = str(case)  # Explicit conversion to string and debugging
            switch_statement += f"\t{case_str}\n"
        switch_statement += f"\tdefault return {self.RGBColor}"
        return switch_statement
    

class CoverageConstructor:
    """
    Allows users to create own Coverages instead of using from provided Coverages in WCPS
    """

    def __init__(self, new_name, expression, x_axis=None, y_axis=None):
        """
        Initialize a new CoverageConstructor instance.

        Args:
            new_name (str): The name of the new coverage to be created.
            expression (str): The expression defining the values of the coverage.
            x_axis (tuple, optional): Tuple specifying the range of values for the x-axis.
                                       Defaults to (0, 200) if not provided.
            y_axis (tuple, optional): Tuple specifying the range of values for the y-axis.
                                       Defaults to (0, 200) if not provided.
        """
        # Set default axis values if not provided
        x_axis = x_axis or (0, 200)
        y_axis = y_axis or (0, 200)

        self.x_axis_obj = Axis('x', x_axis[0], x_axis[1])
        self.y_axis_obj = Axis('y', y_axis[0], y_axis[1])
        self.new_name = new_name
        self.expression = expression

    def __str__(self):
        """
        Returns a string representation of the CoverageConstructor instance.

        Returns:
            str: A string representing the coverage expression.
        """
        coverage_expression = f"values {self.expression}"
        coverage_expression = f"over $x {self.x_axis_obj}, $y {self.y_axis_obj} {coverage_expression}"
        coverage_expression = f"coverage {self.new_name} {coverage_expression}"
        return coverage_expression



class Query:
    """
    Manages operations on a datacube such as querying data through the DatabaseConnection.
    """

    VALID_RETURN_TYPES = {
        'CSV': "text/csv",
        'PNG': "image/png",
        'JPEG': "image/jpeg"
    }

    def __init__(self, dbc):
        """
        Initialize the Query instance with a DatabaseConnection.

        Args:
            dbc (DatabaseConnection): The database connection to use for sending queries.

        Attributes:
            dbc (DatabaseConnection): Stores the database connection object that will be used for querying.
            coverages (list): List to store coverage objects added for the query.
            return_type (str, optional): The type of data to return from queries (CSV, PNG, JPEG), which
                                         needs to match one of the predefined valid return types.
            return_value (str, optional): Specific values or expressions to be returned by the query, used in
                                          conjunction with return_type to format the output.
            operation (str, optional): The operation to be performed on the data (e.g., max, min, average).
                                       This defines the processing step to be applied to the dataset.
            count_condition (str, optional): A condition to be applied specifically for count operations,
                                             defining filters or criteria that count must satisfy.
            Switch (Switch, optional): The switch statement to be used for colorcoding operation.
        """
        self.dbc = dbc
        self.coverages = []
        self.return_type = None
        self.return_value = None
        self.operation = None
        self.count_condition = None
        self.Switch = None

    def add_coverage(self, coverage):
        """
        Add a coverage to the datacube queries.

        Args:
            coverage (Coverage): The coverage object.

        Raises:
            TypeError: If coverage is not an instance of Coverage.
        """
        if not isinstance(coverage, Coverage):
            raise TypeError("coverage must be an instance of Coverage")
        self.coverages.append(coverage)

    def set_return(self, return_type, return_value=None):
        """
        Set the return type and value for the results of the queries.

        Args:
            return_type (str): The type of return (e.g., 'CSV', 'PNG', 'JPEG').
            return_value (str): The value to be returned, used in specific queries.

        Raises:
            ValueError: If the return_type is not valid.
        """
        if return_type in self.VALID_RETURN_TYPES:
            self.return_type = return_type
            self.return_value = return_value
        else:
            raise ValueError(f"Invalid return type. Valid types are: {list(self.VALID_RETURN_TYPES.keys())}")

    def set_operation(self, operation):
        """
        Set the operation to perform on the data.

        Args:
            operation (str): The operation to be performed.

        Raises:
            ValueError: If the operation is not valid.
        """
        if operation in ['max', 'min', 'avg', 'count', 'encode', 'colorcoding', 'constructor']:
            self.operation = operation
        else:
            raise ValueError("Invalid operation.")

    def set_count_condition(self, condition):
        """
        Set the condition for count operations.

        Args:
            condition (str): The condition to be applied in a count operation.
        """
        self.count_condition = condition

    def set_switch(self, switch):
        """
        Set the switch statement for colorcoding operation.

        Args:
            switch (switch): The Switch object representing the switch statement.
        """
        self.switch = switch

    def construct_coverage(self, expression, new_name, x_axis = None, y_axis = None):
        if not self.coverages:
            raise ValueError("At least one coverage must be added before generating the query.")

        base_query = ""
        for coverage in self.coverages:
            if base_query:
                base_query += ",\n"
            base_query += f"${coverage.variable} in ({coverage.name})"  # Include each coverage
        base_query = "for " + base_query + "\n"
        
        if self.operation == 'constructor':
            new_coverage = CoverageConstructor(new_name, expression, x_axis, y_axis)
            return f"{base_query}return encode({new_coverage}, \"{self.VALID_RETURN_TYPES[self.return_type]}\")"
        
        
    def generate_query(self, expression = None):
        """
        Generate the database query based on the set parameters and the provided expression.

        Args:
            expression (str): The expression to be included in the query and used for the operations. Could also be a single coverage.

        Returns:
            str: The generated query string.

        Raises:
            ValueError: If the parameters are insufficient to generate a valid query.
        """
        if not self.coverages:
            raise ValueError("At least one coverage must be added before generating the query.")

        base_query = ""
        for coverage in self.coverages:
            if base_query:
                base_query += ",\n"
            base_query += f"${coverage.variable} in ({coverage.name})"  # Include each coverage
        base_query = "for " + base_query + "\n"

        if self.operation in ['max', 'min', 'avg', 'count', 'encode', 'colorcoding']:
            if self.operation == 'count' and self.count_condition: # Count operation
                return f"{base_query}return count({expression} {self.count_condition})"
            elif self.operation == 'encode' and self.return_type: # Encode operation
                return f"{base_query}return encode({expression}, \"{self.VALID_RETURN_TYPES[self.return_type]}\")"
            elif self.operation == 'colorcoding' and (self.return_type == 'PNG' or self.return_type == 'JPEG') and self.Switch: # Switch operation
                return f"{base_query} return encode(\n    {self.Switch}\n\t, \"{self.VALID_RETURN_TYPES[self.return_type]}\")"
            elif self.operation == 'max' or self.operation == 'min' or self.operation == 'avg' or self.operation == 'count': # Aggregate
                return f"{base_query}return {self.operation}({expression})"

                

        # Most basic query
        elif self.return_value is not None:
            return f"{base_query}return {self.return_value}"

        # Selecting a single value
        elif not self.operation:
            return f"{base_query}return ({expression})"

        else:
            raise ValueError("Insufficient parameters to generate a valid query: check operation, subset parameters, and return types.")

    def execute_query(self, expression):
        """
        Execute the generated query using the DatabaseConnection.

        Args:
            expression (str): The expression to be executed and included in the query and used for the operations. Could also be a single coverage.

        Returns:
            bytes or str: The raw content of the response if successful, or an error message if the request fails.
        """
        query = self.generate_query(expression)  # Generate the query based on current settings
        response = self.dbc.send_request(query)  # Send the query and receive the response
        if response:
            return response.content  # Return the raw content of the response
        else:
            return "Query execution failed or no response."  # Return an error message if the request failed